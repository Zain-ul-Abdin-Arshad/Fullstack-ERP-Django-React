"""
Purchase Order Management Models
Models for managing purchase orders, purchase items, and landed cost calculations
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class PurchaseOrder(models.Model):
    """
    Purchase Order model for managing vendor purchase orders
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RECEIVED', 'Received'),
        ('PARTIAL', 'Partially Received'),
        ('CANCELLED', 'Cancelled'),
    ]

    vendor = models.ForeignKey(
        'vendors.Vendor',
        on_delete=models.PROTECT,
        related_name='purchase_orders',
        verbose_name=_("Vendor"),
        help_text=_("Vendor/supplier for this purchase order")
    )
    order_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Order Number"),
        help_text=_("Unique purchase order number")
    )
    order_date = models.DateField(
        verbose_name=_("Order Date"),
        help_text=_("Date when the purchase order was created")
    )
    expected_delivery_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Expected Delivery Date"),
        help_text=_("Expected date of delivery")
    )
    received_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Received Date"),
        help_text=_("Date when the order was received")
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Total Amount"),
        help_text=_("Total amount of the purchase order")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name=_("Status"),
        help_text=_("Current status of the purchase order")
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Notes"),
        help_text=_("Additional notes about the purchase order")
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
        verbose_name = _("Purchase Order")
        verbose_name_plural = _("Purchase Orders")
        ordering = ['-order_date', '-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['vendor']),
            models.Index(fields=['order_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"PO-{self.order_number} - {self.vendor.name}"

    def calculate_total(self):
        """Calculate total amount from purchase items"""
        total = self.purchase_items.aggregate(
            total=models.Sum('line_total')
        )['total'] or Decimal('0.00')
        self.total_amount = total
        self.save(update_fields=['total_amount'])
        return total

    def get_item_count(self):
        """Get total number of items in the order"""
        return self.purchase_items.count()

    def get_total_quantity(self):
        """Get total quantity of all items"""
        return self.purchase_items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

    def mark_as_received(self):
        """Mark purchase order as received"""
        if self.status != 'RECEIVED':
            self.status = 'RECEIVED'
            from django.utils import timezone
            self.received_date = timezone.now().date()
            self.save(update_fields=['status', 'received_date'])


class PurchaseItem(models.Model):
    """
    Purchase Item model for individual items in a purchase order
    Includes landed cost calculation
    """
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name='purchase_items',
        verbose_name=_("Purchase Order"),
        help_text=_("Purchase order this item belongs to")
    )
    item = models.ForeignKey(
        'inventory.Item',
        on_delete=models.PROTECT,
        related_name='purchase_items',
        verbose_name=_("Item"),
        help_text=_("Product/item being purchased")
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_("Quantity"),
        help_text=_("Quantity of items ordered")
    )
    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Unit Cost"),
        help_text=_("Cost per unit")
    )
    freight_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Freight Cost"),
        help_text=_("Freight/shipping cost allocated to this item")
    )
    customs_duty = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Customs Duty"),
        help_text=_("Customs duty/tariff cost allocated to this item")
    )
    other_costs = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Other Costs"),
        help_text=_("Other costs (insurance, handling, etc.) allocated to this item")
    )
    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        editable=False,
        verbose_name=_("Line Total"),
        help_text=_("Total cost for this line (quantity * unit_cost)")
    )
    landed_cost_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        editable=False,
        verbose_name=_("Landed Cost Per Unit"),
        help_text=_("Total landed cost per unit including all additional costs")
    )
    total_landed_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        editable=False,
        verbose_name=_("Total Landed Cost"),
        help_text=_("Total landed cost for this line item")
    )
    received_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Received Quantity"),
        help_text=_("Quantity actually received")
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
        verbose_name = _("Purchase Item")
        verbose_name_plural = _("Purchase Items")
        ordering = ['purchase_order', 'item']
        indexes = [
            models.Index(fields=['purchase_order']),
            models.Index(fields=['item']),
        ]

    def __str__(self):
        return f"{self.purchase_order.order_number} - {self.item.name} x{self.quantity}"

    def calculate_line_total(self):
        """Calculate line total (quantity * unit_cost)"""
        return self.quantity * self.unit_cost

    def calculate_landed_cost(self):
        """
        Calculate landed cost per unit and total landed cost
        
        Landed Cost = Unit Cost + (Freight Cost + Customs Duty + Other Costs) / Quantity
        Total Landed Cost = Landed Cost Per Unit * Quantity
        """
        # Calculate additional costs per unit
        additional_costs = self.freight_cost + self.customs_duty + self.other_costs
        additional_cost_per_unit = additional_costs / Decimal(str(self.quantity)) if self.quantity > 0 else Decimal('0.00')
        
        # Landed cost per unit = unit cost + additional costs per unit
        self.landed_cost_per_unit = self.unit_cost + additional_cost_per_unit
        
        # Total landed cost = landed cost per unit * quantity
        self.total_landed_cost = self.landed_cost_per_unit * Decimal(str(self.quantity))
        
        return {
            'landed_cost_per_unit': self.landed_cost_per_unit,
            'total_landed_cost': self.total_landed_cost
        }

    def save(self, *args, **kwargs):
        """Override save to calculate line total and landed costs"""
        # Calculate line total
        self.line_total = self.calculate_line_total()
        
        # Calculate landed costs
        self.calculate_landed_cost()
        
        super().save(*args, **kwargs)
        
        # Update purchase order total
        if self.purchase_order:
            self.purchase_order.calculate_total()

    def get_cost_breakdown(self):
        """Get detailed cost breakdown for this item"""
        return {
            'unit_cost': self.unit_cost,
            'quantity': self.quantity,
            'subtotal': self.line_total,
            'freight_cost': self.freight_cost,
            'customs_duty': self.customs_duty,
            'other_costs': self.other_costs,
            'total_additional_costs': self.freight_cost + self.customs_duty + self.other_costs,
            'landed_cost_per_unit': self.landed_cost_per_unit,
            'total_landed_cost': self.total_landed_cost,
        }

    def is_fully_received(self):
        """Check if item is fully received"""
        return self.received_quantity >= self.quantity

    def get_pending_quantity(self):
        """Get pending quantity to be received"""
        return max(0, self.quantity - self.received_quantity)

