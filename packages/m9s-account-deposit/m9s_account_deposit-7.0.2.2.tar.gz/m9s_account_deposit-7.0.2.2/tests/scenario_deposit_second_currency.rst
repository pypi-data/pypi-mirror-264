=====================================
Deposit with Second Currency Scenario
=====================================

Imports::

    >>> import datetime as dt
    >>> from decimal import Decimal

    >>> from proteus import Model
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.currency.tests.tools import get_currency
    >>> from trytond.modules.company.tests.tools import create_company
    >>> from trytond.modules.account.tests.tools import (
    ...     create_fiscalyear, create_chart, get_accounts)
    >>> from trytond.modules.account_invoice.tests.tools import (
    ...     set_fiscalyear_invoice_sequences, create_payment_term)
    >>> from trytond.modules.account_deposit.tests.tools import (
    ...     add_deposit_accounts)
    >>> today = dt.date.today()
    >>> yesterday = today - dt.timedelta(days=1)

Activate modules::

    >>> config = activate_modules('account_deposit')

    >>> Party = Model.get('party.party')
    >>> Invoice = Model.get('account.invoice')

Create company::

    >>> currency = get_currency('USD')
    >>> eur = get_currency('EUR')
    >>> _ = create_company(currency=currency)

Set alternate currency rates::

    >>> rate = eur.rates.new()
    >>> rate.date = yesterday
    >>> rate.rate = Decimal('1.20')
    >>> rate = eur.rates.new()
    >>> rate.date = today
    >>> rate.rate = Decimal('1.10')
    >>> eur.save()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(create_fiscalyear())
    >>> fiscalyear.click('create_period')

Create chart of accounts::

    >>> _ = create_chart()
    >>> accounts = add_deposit_accounts(get_accounts())
    >>> accounts['deposit'].second_currency = eur
    >>> accounts['deposit'].save()

Create party::

    >>> party = Party(name='Party')
    >>> party.save()

Configure the default deposit account::

    >>> AccountConfiguration = Model.get('account.configuration')
    >>> configuration = AccountConfiguration(1)
    >>> configuration.default_account_deposit = accounts['deposit']
    >>> configuration.save()

Create deposit invoice::

    >>> invoice = Invoice(party=party, currency=eur, invoice_date=yesterday)
    >>> line = invoice.lines.new()
    >>> line.account = accounts['deposit']
    >>> line.description = "Deposit"
    >>> line.quantity = 1
    >>> line.unit_price = Decimal(100)
    >>> invoice.click('post')
    >>> invoice.untaxed_amount
    Decimal('100.00')

Check party deposit::

    >>> party.reload()
    >>> party.deposit
    Decimal('83.33')

Create final invoice::

    >>> invoice = Invoice(party=party, currency=eur, invoice_date=today)
    >>> line = invoice.lines.new()
    >>> line.account = accounts['revenue']
    >>> line.description = "Revenue"
    >>> line.quantity = 1
    >>> line.unit_price = Decimal(500)
    >>> invoice.save()
    >>> invoice.untaxed_amount
    Decimal('500.00')

Manage deposit (automatically on write)::

    >>> invoice.save()
    >>> invoice.description = 'managed'
    >>> invoice.save()
    >>> invoice.reload()
    >>> deposit_line, = [l for l in invoice.lines
    ...     if l.account == accounts['deposit']]
    >>> deposit_line.amount
    Decimal('-91.66')
    >>> invoice.untaxed_amount
    Decimal('408.34')
    >>> invoice.click('post')

Check party deposit::

    >>> party.reload()
    >>> party.deposit
    Decimal('0.00')
    >>> accounts['deposit'].reload()
    >>> accounts['deposit'].balance
    Decimal('0.00')
    >>> accounts['deposit'].amount_second_currency
    Decimal('-8.34')
