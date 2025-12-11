# Accounts Models - Quick Reference

## Models Created

✅ **Payment** - Payment transactions (vendor/client)  
✅ **LedgerEntry** - Double-entry bookkeeping ledger  
✅ **ProfitLoss** - Profit/loss calculation and reporting

## Required Fields

### Payment
- `vendor` (FK, nullable) ✅
- `client` (FK, nullable) ✅
- `amount` ✅
- `payment_type` (CREDIT/DEBIT) ✅
- `date` ✅
- `description` ✅

## Payment Types

- `CREDIT` - Money coming in (revenue, client payments)
- `DEBIT` - Money going out (expenses, vendor payments)

## Quick Usage

```python
from accounts.models import Payment, LedgerEntry, ProfitLoss
from clients.models import Client
from vendors.models import Vendor
from datetime import date

# Create Client Payment (CREDIT - money in)
client = Client.objects.get(name="ABC Auto Shop")
payment = Payment.objects.create(
    client=client,
    amount=5000.00,
    payment_type='CREDIT',
    date=date.today(),
    description="Payment for invoice"
)
# Ledger entry automatically created

# Create Vendor Payment (DEBIT - money out)
vendor = Vendor.objects.get(name="ABC Suppliers")
payment = Payment.objects.create(
    vendor=vendor,
    amount=3000.00,
    payment_type='DEBIT',
    date=date.today(),
    description="Payment for purchase"
)
# Ledger entry automatically created
```

## Ledger Tracking

### Automatic Creation

- Payments → Ledger entries created automatically
- Sales Orders (SHIPPED/DELIVERED) → Ledger entries via signal
- Purchase Orders (RECEIVED) → Ledger entries via signal

### Manual Ledger Operations

```python
# Get totals for period
start_date = date.today().replace(day=1)
end_date = date.today()

total_debits = LedgerEntry.get_total_debits(start_date, end_date)
total_credits = LedgerEntry.get_total_credits(start_date, end_date)
balance = LedgerEntry.get_balance(start_date, end_date)
```

## Profit/Loss Calculation

### Formula

```
Revenue = Sales Orders (SHIPPED/DELIVERED)
COGS = Purchase Orders (RECEIVED)
Expenses = DEBIT Payments

Gross Profit = Revenue - COGS
Net Profit = Gross Profit - Expenses
```

### Usage

```python
from accounts.models import ProfitLoss
from datetime import date

# Calculate P&L
start_date = date.today().replace(day=1)
end_date = date.today()

# Calculate without saving
p_l = ProfitLoss.calculate_profit_loss(start_date, end_date)
print(f"Net Profit: ${p_l['net_profit']}")

# Create and save report
report = ProfitLoss.create_report(start_date, end_date)
```

## Validation Rules

- Payment: Either vendor OR client must be specified (not both)
- Payment: Amount must be > 0
- Ledger: At least one amount (debit/credit) must be > 0

## Files Created

- `backend/accounts/models.py` - Accounts models
- `backend/accounts/admin.py` - Admin configuration

## Next Steps

```powershell
# Create migrations
python manage.py makemigrations accounts

# Apply migrations
python manage.py migrate
```

## Example: Complete Payment Flow

```python
# 1. Create Client Payment (CREDIT)
payment = Payment.objects.create(
    client=client,
    amount=5000.00,
    payment_type='CREDIT',
    date=date.today(),
    description="Invoice payment"
)

# 2. Ledger entry auto-created
ledger_entries = payment.ledger_entries.all()

# 3. Calculate P&L for month
report = ProfitLoss.create_report(start_date, end_date)
print(f"Net Profit: ${report.net_profit}")
```

