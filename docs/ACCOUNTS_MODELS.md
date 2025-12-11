# Accounts Models Documentation

Complete Django models for managing payments, ledger entries, and profit/loss calculations.

## Models Overview

1. **Payment** - Payment transactions (vendor/client payments)
2. **LedgerEntry** - Double-entry bookkeeping ledger entries
3. **ProfitLoss** - Profit/loss calculation and reporting

## Model Relationships

```
Vendor (1) ──→ (N) Payment (nullable)
Client (1) ──→ (N) Payment (nullable)
Payment (1) ──→ (N) LedgerEntry
PurchaseOrder (1) ──→ (N) Payment (nullable)
SalesOrder (1) ──→ (N) Payment (nullable)
```

## Payment Model

### Required Fields (As Requested)

- `vendor` - Foreign key to Vendor (nullable) ✅
- `client` - Foreign key to Client (nullable) ✅
- `amount` - Payment amount (DecimalField, required) ✅
- `payment_type` - Credit/Debit (CharField with choices, required) ✅
- `date` - Payment date (DateField, required) ✅
- `description` - Payment description (TextField, required) ✅

### Additional Fields

- `payment_method` - Method of payment (Cash, Bank Transfer, etc.)
- `reference_number` - Transaction reference number
- `purchase_order` - Related purchase order (nullable)
- `sales_order` - Related sales order (nullable)
- `is_reconciled` - Reconciliation status
- `created_at`, `updated_at` - Timestamps

### Payment Type Choices

- `CREDIT` - Money coming in (revenue, client payments)
- `DEBIT` - Money going out (expenses, vendor payments)

### Payment Method Choices

- `CASH` - Cash payment
- `BANK_TRANSFER` - Bank transfer
- `CHEQUE` - Cheque payment
- `CREDIT_CARD` - Credit card
- `DEBIT_CARD` - Debit card
- `ONLINE` - Online payment
- `OTHER` - Other payment method

### Validation

- Either `vendor` OR `client` must be specified (not both, not neither)
- Amount must be greater than 0
- Automatic ledger entry creation on save

## LedgerEntry Model

### Purpose

Tracks all financial transactions using double-entry bookkeeping principles.

### Fields

- `payment` - Related payment (nullable)
- `date` - Entry date
- `description` - Entry description
- `debit_amount` - Debit amount (money out)
- `credit_amount` - Credit amount (money in)
- `entry_type` - Type of entry (PAYMENT, SALES, PURCHASE, etc.)
- `reference_type` - Type of reference object
- `reference_id` - ID of reference object
- `created_at` - Creation timestamp

### Entry Type Choices

- `PAYMENT` - Payment transaction
- `SALES` - Sales order
- `PURCHASE` - Purchase order
- `ADJUSTMENT` - Manual adjustment
- `OTHER` - Other entry type

### Class Methods

- `get_total_debits(start_date, end_date)` - Get total debits for period
- `get_total_credits(start_date, end_date)` - Get total credits for period
- `get_balance(start_date, end_date)` - Get balance (credits - debits)
- `create_sales_entry(sales_order)` - Create entry for sales order
- `create_purchase_entry(purchase_order)` - Create entry for purchase order

## ProfitLoss Model

### Purpose

Stores calculated profit/loss reports for reporting periods.

### Fields

- `period_start` - Start date of period
- `period_end` - End date of period
- `total_revenue` - Total sales revenue
- `total_cost_of_goods_sold` - Total COGS
- `total_expenses` - Total operating expenses
- `gross_profit` - Gross profit (Revenue - COGS)
- `net_profit` - Net profit (Gross Profit - Expenses)
- `created_at` - Creation timestamp

### Class Methods

- `calculate_profit_loss(start_date, end_date)` - Calculate P&L for period
- `create_report(start_date, end_date)` - Create and save P&L report

## Ledger Tracking

### Automatic Ledger Entry Creation

Ledger entries are automatically created for:

1. **Payments** - When a payment is created, a ledger entry is automatically created
2. **Sales Orders** - When a sales order is shipped/delivered (via signal)
3. **Purchase Orders** - When a purchase order is received (via signal)

### Ledger Entry Logic

```python
# Payment creates ledger entry
Payment (CREDIT, $1000)
→ LedgerEntry (credit_amount=$1000, debit_amount=$0)

Payment (DEBIT, $500)
→ LedgerEntry (credit_amount=$0, debit_amount=$500)

# Sales Order creates ledger entry
SalesOrder (total=$5000, status=SHIPPED)
→ LedgerEntry (credit_amount=$5000, debit_amount=$0)

# Purchase Order creates ledger entry
PurchaseOrder (total=$3000, status=RECEIVED)
→ LedgerEntry (credit_amount=$0, debit_amount=$3000)
```

## Profit/Loss Calculation

### Formula

```
Revenue = Sum of all Sales Orders (SHIPPED/DELIVERED)
Cost of Goods Sold (COGS) = Sum of all Purchase Orders (RECEIVED)
Expenses = Sum of all DEBIT payments

Gross Profit = Revenue - COGS
Net Profit = Gross Profit - Expenses
```

### Calculation Method

The `calculate_profit_loss()` method:
1. Calculates total revenue from shipped/delivered sales orders
2. Calculates COGS from received purchase orders
3. Calculates expenses from debit payments
4. Calculates gross profit (Revenue - COGS)
5. Calculates net profit (Gross Profit - Expenses)

## Usage Examples

### Creating a Payment (Client Payment - Credit)

```python
from accounts.models import Payment
from clients.models import Client
from datetime import date

# Get client
client = Client.objects.get(name="ABC Auto Shop")

# Create payment (money coming in - CREDIT)
payment = Payment.objects.create(
    client=client,
    amount=5000.00,
    payment_type='CREDIT',
    payment_method='BANK_TRANSFER',
    date=date.today(),
    description="Payment for invoice #12345",
    reference_number="TXN-2024-001"
)
# Ledger entry automatically created
```

### Creating a Payment (Vendor Payment - Debit)

```python
from vendors.models import Vendor

# Get vendor
vendor = Vendor.objects.get(name="ABC Suppliers")

# Create payment (money going out - DEBIT)
payment = Payment.objects.create(
    vendor=vendor,
    amount=3000.00,
    payment_type='DEBIT',
    payment_method='CHEQUE',
    date=date.today(),
    description="Payment for purchase order PO-001",
    reference_number="CHQ-2024-001"
)
# Ledger entry automatically created
```

### Querying Payments

```python
# Get all credit payments (money in)
credits = Payment.objects.filter(payment_type='CREDIT')

# Get all debit payments (money out)
debits = Payment.objects.filter(payment_type='DEBIT')

# Get payments by client
client_payments = Payment.objects.filter(client=client)

# Get payments by vendor
vendor_payments = Payment.objects.filter(vendor=vendor)

# Get payments by date range
from datetime import date, timedelta
start_date = date.today() - timedelta(days=30)
recent_payments = Payment.objects.filter(date__gte=start_date)
```

### Ledger Entry Operations

```python
from accounts.models import LedgerEntry
from datetime import date, timedelta

# Get total debits for current month
start_date = date.today().replace(day=1)
end_date = date.today()
total_debits = LedgerEntry.get_total_debits(start_date, end_date)

# Get total credits for current month
total_credits = LedgerEntry.get_total_credits(start_date, end_date)

# Get balance (credits - debits)
balance = LedgerEntry.get_balance(start_date, end_date)

# Get all ledger entries for period
entries = LedgerEntry.objects.filter(
    date__gte=start_date,
    date__lte=end_date
).order_by('date')
```

### Calculating Profit/Loss

```python
from accounts.models import ProfitLoss
from datetime import date, timedelta

# Calculate profit/loss for current month
start_date = date.today().replace(day=1)
end_date = date.today()

# Calculate without saving
p_l_data = ProfitLoss.calculate_profit_loss(start_date, end_date)
print(f"Revenue: ${p_l_data['total_revenue']}")
print(f"COGS: ${p_l_data['total_cost_of_goods_sold']}")
print(f"Expenses: ${p_l_data['total_expenses']}")
print(f"Gross Profit: ${p_l_data['gross_profit']}")
print(f"Net Profit: ${p_l_data['net_profit']}")

# Create and save report
report = ProfitLoss.create_report(start_date, end_date)
print(f"Report created: {report}")
```

### Manual Ledger Entry Creation

```python
from accounts.models import LedgerEntry
from decimal import Decimal

# Create manual ledger entry
entry = LedgerEntry.objects.create(
    date=date.today(),
    description="Manual adjustment",
    debit_amount=Decimal('0.00'),
    credit_amount=Decimal('100.00'),
    entry_type='ADJUSTMENT'
)
```

### Creating Ledger Entries for Orders

```python
from sales.models import SalesOrder
from purchases.models import PurchaseOrder

# Get orders
sales_order = SalesOrder.objects.get(order_number="SO-001")
purchase_order = PurchaseOrder.objects.get(order_number="PO-001")

# Create ledger entries (if not auto-created)
if sales_order.status in ['SHIPPED', 'DELIVERED']:
    LedgerEntry.create_sales_entry(sales_order)

if purchase_order.status == 'RECEIVED':
    LedgerEntry.create_purchase_entry(purchase_order)
```

## Financial Reports

### Revenue Report

```python
from sales.models import SalesOrder
from datetime import date, timedelta

start_date = date.today().replace(day=1)
end_date = date.today()

revenue = SalesOrder.objects.filter(
    order_date__gte=start_date,
    order_date__lte=end_date,
    status__in=['SHIPPED', 'DELIVERED']
).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
```

### Expenses Report

```python
from accounts.models import Payment

expenses = Payment.objects.filter(
    date__gte=start_date,
    date__lte=end_date,
    payment_type='DEBIT'
).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
```

### Complete P&L Report

```python
from accounts.models import ProfitLoss

# Generate monthly report
report = ProfitLoss.create_report(start_date, end_date)

# Access report data
print(f"Period: {report.period_start} to {report.period_end}")
print(f"Revenue: ${report.total_revenue}")
print(f"COGS: ${report.total_cost_of_goods_sold}")
print(f"Gross Profit: ${report.gross_profit}")
print(f"Expenses: ${report.total_expenses}")
print(f"Net Profit: ${report.net_profit}")
```

## Validation Rules

### Payment Validation

1. Either `vendor` OR `client` must be specified (not both, not neither)
2. Amount must be greater than 0
3. Date must be provided

### Ledger Entry Validation

1. At least one of `debit_amount` or `credit_amount` must be greater than 0
2. Both amounts cannot be 0

## Admin Interface

All models are registered in Django Admin with:
- List displays with key fields
- Search functionality
- Filters for dates, types, parties
- Read-only calculated fields
- Autocomplete for related objects

## Migration Commands

```powershell
# Create migrations
python manage.py makemigrations accounts

# Apply migrations
python manage.py migrate

# Check for issues
python manage.py check
```

## Best Practices

1. **Always specify vendor OR client** - Payments must be linked to a party
2. **Use correct payment type** - CREDIT for money in, DEBIT for money out
3. **Link to orders** - Link payments to purchase/sales orders when applicable
4. **Reconcile payments** - Mark payments as reconciled after bank reconciliation
5. **Regular P&L reports** - Generate monthly/quarterly profit/loss reports
6. **Review ledger entries** - Regularly review ledger entries for accuracy

## Integration with Other Modules

- **Sales** - Automatic ledger entries for sales orders
- **Purchases** - Automatic ledger entries for purchase orders
- **Vendors** - Vendor payment tracking
- **Clients** - Client payment tracking

## Next Steps

1. Create serializers for REST API
2. Create viewsets for CRUD operations
3. Add payment reconciliation features
4. Create financial reporting views
5. Add invoice generation
6. Implement payment reminders
7. Add bank reconciliation features

