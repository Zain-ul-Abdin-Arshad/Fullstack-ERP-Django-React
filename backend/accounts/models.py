"""
Accounts Management Models
Models for managing payments, ledger entries, and profit/loss calculations
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Q
from decimal import Decimal


class Payment(models.Model):
    """
    Payment model for tracking payments to vendors and from clients
    """
    PAYMENT_TYPE_CHOICES = [
        ('CREDIT', 'Credit'),
        ('DEBIT', 'Debit'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('ONLINE', 'Online Payment'),
        ('OTHER', 'Other'),
    ]

    vendor = models.ForeignKey(
        'vendors.Vendor',
        on_delete=models.PROTECT,
        related_name='payments',
        blank=True,
        null=True,
        verbose_name=_("Vendor"),
        help_text=_("Vendor/supplier for vendor payments")
    )
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.PROTECT,
        related_name='payments',
        blank=True,
        null=True,
        verbose_name=_("Client"),
        help_text=_("Client/customer for client payments")
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_("Amount"),
        help_text=_("Payment amount")
    )
    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_TYPE_CHOICES,
        verbose_name=_("Payment Type"),
        help_text=_("Credit (money in) or Debit (money out)")
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='BANK_TRANSFER',
        verbose_name=_("Payment Method"),
        help_text=_("Method of payment")
    )
    date = models.DateField(
        verbose_name=_("Payment Date"),
        help_text=_("Date of the payment")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Description or notes about the payment")
    )
    reference_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Reference Number"),
        help_text=_("Transaction reference number (check number, transfer ID, etc.)")
    )
    purchase_order = models.ForeignKey(
        'purchases.PurchaseOrder',
        on_delete=models.SET_NULL,
        related_name='payments',
        blank=True,
        null=True,
        verbose_name=_("Purchase Order"),
        help_text=_("Related purchase order (if applicable)")
    )
    sales_order = models.ForeignKey(
        'sales.SalesOrder',
        on_delete=models.SET_NULL,
        related_name='payments',
        blank=True,
        null=True,
        verbose_name=_("Sales Order"),
        help_text=_("Related sales order (if applicable)")
    )
    is_reconciled = models.BooleanField(
        default=False,
        verbose_name=_("Is Reconciled"),
        help_text=_("Whether this payment has been reconciled")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['vendor']),
            models.Index(fields=['client']),
            models.Index(fields=['date']),
            models.Index(fields=['payment_type']),
            models.Index(fields=['purchase_order']),
            models.Index(fields=['sales_order']),
        ]

    def __str__(self):
        if self.vendor:
            return f"{self.payment_type} - {self.vendor.name} - ${self.amount}"
        elif self.client:
            return f"{self.payment_type} - {self.client.name} - ${self.amount}"
        return f"{self.payment_type} - ${self.amount}"

    def clean(self):
        """Validate that either vendor or client is set, but not both"""
        from django.core.exceptions import ValidationError
        if not self.vendor and not self.client:
            raise ValidationError("Either vendor or client must be specified.")
        if self.vendor and self.client:
            raise ValidationError("Payment cannot be for both vendor and client.")

    def save(self, *args, **kwargs):
        """Override save to create ledger entry"""
        self.full_clean()  # Run validation
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Create ledger entry
        if is_new:
            self.create_ledger_entry()

    def create_ledger_entry(self):
        """Create ledger entry for this payment"""
        LedgerEntry.objects.create(
            payment=self,
            date=self.date,
            description=self.description,
            debit_amount=self.amount if self.payment_type == 'DEBIT' else Decimal('0.00'),
            credit_amount=self.amount if self.payment_type == 'CREDIT' else Decimal('0.00'),
            reference_type='PAYMENT',
            reference_id=self.id
        )


class LedgerEntry(models.Model):
    """
    Ledger Entry model for double-entry bookkeeping
    Tracks all financial transactions
    """
    ENTRY_TYPE_CHOICES = [
        ('PAYMENT', 'Payment'),
        ('SALES', 'Sales'),
        ('PURCHASE', 'Purchase'),
        ('ADJUSTMENT', 'Adjustment'),
        ('OTHER', 'Other'),
    ]

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='ledger_entries',
        blank=True,
        null=True,
        verbose_name=_("Payment"),
        help_text=_("Related payment (if applicable)")
    )
    date = models.DateField(
        verbose_name=_("Entry Date"),
        help_text=_("Date of the ledger entry")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Description of the ledger entry")
    )
    debit_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Debit Amount"),
        help_text=_("Debit amount (money out)")
    )
    credit_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Credit Amount"),
        help_text=_("Credit amount (money in)")
    )
    entry_type = models.CharField(
        max_length=20,
        choices=ENTRY_TYPE_CHOICES,
        default='OTHER',
        verbose_name=_("Entry Type"),
        help_text=_("Type of ledger entry")
    )
    reference_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Reference Type"),
        help_text=_("Type of reference (e.g., PAYMENT, SALES_ORDER)")
    )
    reference_id = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("Reference ID"),
        help_text=_("ID of the referenced object")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )

    class Meta:
        verbose_name = _("Ledger Entry")
        verbose_name_plural = _("Ledger Entries")
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['entry_type']),
            models.Index(fields=['reference_type', 'reference_id']),
        ]

    def __str__(self):
        return f"{self.date} - {self.description[:50]} - D:{self.debit_amount} C:{self.credit_amount}"

    @classmethod
    def get_total_debits(cls, start_date=None, end_date=None):
        """Get total debits for a date range"""
        queryset = cls.objects.all()
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        return queryset.aggregate(total=Sum('debit_amount'))['total'] or Decimal('0.00')

    @classmethod
    def get_total_credits(cls, start_date=None, end_date=None):
        """Get total credits for a date range"""
        queryset = cls.objects.all()
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        return queryset.aggregate(total=Sum('credit_amount'))['total'] or Decimal('0.00')

    @classmethod
    def get_balance(cls, start_date=None, end_date=None):
        """Get balance (credits - debits) for a date range"""
        credits = cls.get_total_credits(start_date, end_date)
        debits = cls.get_total_debits(start_date, end_date)
        return credits - debits

    @classmethod
    def create_sales_entry(cls, sales_order):
        """Create ledger entry for sales order"""
        return cls.objects.create(
            date=sales_order.order_date,
            description=f"Sales Order {sales_order.order_number}",
            credit_amount=sales_order.total_amount,
            debit_amount=Decimal('0.00'),
            entry_type='SALES',
            reference_type='SALES_ORDER',
            reference_id=sales_order.id
        )

    @classmethod
    def create_purchase_entry(cls, purchase_order):
        """Create ledger entry for purchase order"""
        return cls.objects.create(
            date=purchase_order.order_date,
            description=f"Purchase Order {purchase_order.order_number}",
            debit_amount=purchase_order.total_amount,
            credit_amount=Decimal('0.00'),
            entry_type='PURCHASE',
            reference_type='PURCHASE_ORDER',
            reference_id=purchase_order.id
        )


class ProfitLoss(models.Model):
    """
    Profit/Loss calculation model
    Stores calculated profit/loss for reporting periods
    """
    period_start = models.DateField(
        verbose_name=_("Period Start"),
        help_text=_("Start date of the reporting period")
    )
    period_end = models.DateField(
        verbose_name=_("Period End"),
        help_text=_("End date of the reporting period")
    )
    total_revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_("Total Revenue"),
        help_text=_("Total sales revenue")
    )
    total_cost_of_goods_sold = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_("Cost of Goods Sold"),
        help_text=_("Total cost of goods sold")
    )
    total_expenses = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_("Total Expenses"),
        help_text=_("Total operating expenses")
    )
    gross_profit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_("Gross Profit"),
        help_text=_("Gross profit (Revenue - COGS)")
    )
    net_profit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_("Net Profit"),
        help_text=_("Net profit (Gross Profit - Expenses)")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )

    class Meta:
        verbose_name = _("Profit/Loss")
        verbose_name_plural = _("Profit/Loss Reports")
        ordering = ['-period_end']
        unique_together = [['period_start', 'period_end']]

    def __str__(self):
        return f"P&L {self.period_start} to {self.period_end} - Net: ${self.net_profit}"

    @classmethod
    def calculate_profit_loss(cls, start_date, end_date):
        """
        Calculate profit/loss for a date range
        
        Returns:
            dict with revenue, cogs, expenses, gross_profit, net_profit
        """
        from sales.models import SalesOrder
        from purchases.models import PurchaseOrder
        
        # Calculate total revenue from sales orders
        total_revenue = SalesOrder.objects.filter(
            order_date__gte=start_date,
            order_date__lte=end_date,
            status__in=['SHIPPED', 'DELIVERED']
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
        
        # Calculate cost of goods sold from purchase orders
        total_cogs = PurchaseOrder.objects.filter(
            order_date__gte=start_date,
            order_date__lte=end_date,
            status__in=['RECEIVED']
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
        
        # Calculate expenses (debit payments)
        total_expenses = Payment.objects.filter(
            date__gte=start_date,
            date__lte=end_date,
            payment_type='DEBIT'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Calculate gross profit
        gross_profit = total_revenue - total_cogs
        
        # Calculate net profit
        net_profit = gross_profit - total_expenses
        
        return {
            'total_revenue': total_revenue,
            'total_cost_of_goods_sold': total_cogs,
            'total_expenses': total_expenses,
            'gross_profit': gross_profit,
            'net_profit': net_profit,
        }

    @classmethod
    def create_report(cls, start_date, end_date):
        """Create and save profit/loss report"""
        data = cls.calculate_profit_loss(start_date, end_date)
        
        report, created = cls.objects.update_or_create(
            period_start=start_date,
            period_end=end_date,
            defaults=data
        )
        return report


# Signals to automatically create ledger entries for sales and purchases
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='sales.SalesOrder')
def create_sales_ledger_entry(sender, instance, created, **kwargs):
    """Create ledger entry when sales order is created"""
    if created and instance.status in ['SHIPPED', 'DELIVERED']:
        LedgerEntry.create_sales_entry(instance)

@receiver(post_save, sender='purchases.PurchaseOrder')
def create_purchase_ledger_entry(sender, instance, created, **kwargs):
    """Create ledger entry when purchase order is created"""
    if created and instance.status == 'RECEIVED':
        LedgerEntry.create_purchase_entry(instance)

