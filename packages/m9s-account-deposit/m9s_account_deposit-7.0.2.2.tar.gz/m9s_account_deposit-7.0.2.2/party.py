# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal

from sql import For, Literal, Null
from sql.aggregate import Sum
from sql.conditionals import Case, Coalesce

from trytond.i18n import gettext
from trytond.model import fields
from trytond.modules.currency.fields import Monetary
from trytond.modules.party.exceptions import EraseError
from trytond.pool import Pool, PoolMeta
from trytond.tools import grouped_slice, reduce_ids
from trytond.transaction import Transaction


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    deposit = fields.Function(Monetary(
            "Deposit", currency='currency', digits='currency'),
        'get_deposit', searcher='search_deposit')

    @classmethod
    def get_deposit(cls, parties, name):
        '''
        Function to compute deposit for party ids.
        Adapted from account/party/search_receivable_payable
        '''
        pool = Pool()
        MoveLine = pool.get('account.move.line')
        Account = pool.get('account.account')
        AccountType = pool.get('account.account.type')
        User = pool.get('res.user')
        cursor = Transaction().connection.cursor()

        line = MoveLine.__table__()
        account = Account.__table__()
        account_type = AccountType.__table__()

        result = {p.id: Decimal(0) for p in parties}

        user = User(Transaction().user)
        if not user.company:
            return result
        company_id = user.company.id
        exp = Decimal(str(10.0 ** -user.company.currency.digits))

        # Use credit - debit to display positive deposit amounts
        amount = Sum(Coalesce(line.credit, 0) - Coalesce(line.debit, 0))
        code = name
        for sub_parties in grouped_slice(parties):
            sub_ids = [p.id for p in sub_parties]
            party_where = reduce_ids(line.party, sub_ids)
            cursor.execute(*line.join(account,
                    condition=account.id == line.account
                    ).join(account_type,
                    condition=account.type == account_type.id
                    ).select(line.party, amount,
                    where=(getattr(account_type, code)
                        & (line.reconciliation == Null)
                        & (account.company == company_id)
                        & party_where),
                    group_by=line.party))
            for party, value in cursor:
                # SQLite uses float for SUM
                if not isinstance(value, Decimal):
                    value = Decimal(str(value))
                result[party] = value.quantize(exp)
        return result

    @classmethod
    def search_deposit(cls, name, clause):
        pool = Pool()
        MoveLine = pool.get('account.move.line')
        Account = pool.get('account.account')
        AccountType = pool.get('account.account.type')
        User = pool.get('res.user')

        line = MoveLine.__table__()
        account = Account.__table__()
        account_type = AccountType.__table__()

        _, operator, value = clause

        user = User(Transaction().user)
        if not user.company:
            return []
        company_id = user.company.id
        code = 'deposit'
        Operator = fields.SQL_OPERATORS[operator]

        # Need to cast numeric for sqlite
        cast_ = MoveLine.debit.sql_cast
        amount = cast_(Sum(Coalesce(line.credit, 0) - Coalesce(line.debit, 0)))
        if operator in {'in', 'not in'}:
            value = [cast_(Literal(Decimal(v or 0))) for v in value]
        else:
            value = cast_(Literal(Decimal(value or 0)))
        query = (line.join(account, condition=account.id == line.account
                ).join(account_type, condition=account.type == account_type.id
                ).select(line.party,
                where=(getattr(account_type, code)
                    & (line.party != Null)
                    & (line.reconciliation == Null)
                    & (account.company == company_id)),
                group_by=line.party,
                having=Operator(amount, value)))
        return [('id', 'in', query)]

    def get_deposit_balance(self, deposit_account, currency=None):
        'Return the deposit account balance (debit - credit) for the party'
        pool = Pool()
        MoveLine = pool.get('account.move.line')
        transaction = Transaction()
        cursor = transaction.connection.cursor()

        line = MoveLine.__table__()
        if currency is None:
            currency = deposit_account.currency
        assert deposit_account.type.deposit

        where = ((line.account == deposit_account.id)
            & (line.party == self.id)
            & (line.reconciliation == Null))
        if transaction.database.has_select_for():
            cursor.execute(*line.select(
                    Literal(1),
                    where=where,
                    for_=For('UPDATE', nowait=True)))
        else:
            MoveLine.lock()

        if currency == deposit_account.currency:
            amount = Sum(Coalesce(line.debit, 0) - Coalesce(line.credit, 0))
        else:
            amount = Sum(Case(
                    (line.second_currency == currency.id,
                        line.amount_second_currency),
                    else_=0))

        cursor.execute(*line.select(amount, where=where))
        amount, = cursor.fetchone()
        if amount is None:
            amount = Decimal(0)
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        return currency.round(amount)

    def check_deposit(self, deposit_account, sign=1, deposit_used=None):
        assert sign in (1, -1)
        deposit_available = self.get_deposit_balance(deposit_account)
        if deposit_used is None:
            # Check if the deposit account balance (debit - credit)
            # has the same sign for the party
            return not deposit_available or (
                (deposit_available < 0) == (sign < 0))
        else:
            # Check if the deposit account balance (debit - credit)
            # is sufficient to cover the depsoit_used
            remaining_deposit = deposit_used - (deposit_available * sign)
            return not deposit_available or remaining_deposit < 0


class Erase(metaclass=PoolMeta):
    __name__ = 'party.erase'

    def check_erase_company(self, party, company):
        if party.deposit:
            raise EraseError(
                gettext('account_deposit.msg_erase_party_deposit',
                    party=party.rec_name,
                    company=company.rec_name))
