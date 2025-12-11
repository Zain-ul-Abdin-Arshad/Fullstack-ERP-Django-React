"""
Sales Order Management Models
Models for managing sales orders, sales items, and stock reduction logic
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from decimal import Decimal


class SalesOrder(models.Model):
    """
    Sales Order model for managing customer sales orders
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.PROTECT,
        related_name='sales_orders',
        verbose_name=_("Client"),
        help_text=_("Client/customer for this sales order")
    )
    order_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Order Number"),
        help_text=_("Unique sales order number")
    )
    order_date = models.DateField(
        verbose_name=_("Order Date"),
        help_text=_("Date when the sales order was created")
    )
    expected_delivery_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Expected Delivery Date"),
        help_text=_("Expected date of delivery")
    )
    shipped_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Shipped Date"),
        help_text=_("Date when the order was shipped")
    )
    delivered_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Delivered Date"),
        help_text=_("Date when the order was delivered")
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Total Amount"),
        help_text=_("Total amount of the sales order")
    )
    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Discount Amount"),
        help_text=_("Total discount applied to the order")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name=_("Status"),
        help_text=_("Current status of the sales order")
    )
    warehouse = models.ForeignKey(
        'inventory.Warehouse',
        on_delete=models.PROTECT,
        related_name='sales_orders',
        blank=True,
        null=True,
        verbose_name=_("Warehouse"),
        help_text=_("Warehouse from which items will be shipped")
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Notes"),
        help_text=_("Additional notes about the sales order")
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
        verbose_name = _("Sales Order")
        verbose_name_plural = _("Sales Orders")
        ordering = ['-order_date', '-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['client']),
            models.Index(fields=['order_date']),
            models.Index(fields=['status']),
            models.Index(fields=['warehouse']),
        ]

    def __str__(self):
        return f"SO-{self.order_number} - {self.client.name}"

    def calculate_total(self):
        """Calculate total amount from sales items"""
        total = self.sales_items.aggregate(
            total=models.Sum('line_total')
        )['total'] or Decimal('0.00')
        # Subtract discount
        final_total = total - self.discount_amount
        self.total_amount = max(Decimal('0.00'), final_total)
        self.save(update_fields=['total_amount'])
        return self.total_amount

    def get_item_count(self):
        """Get total number of items in the order"""
        return self.sales_items.count()

    def get_total_quantity(self):
        """Get total quantity of all items"""
        return self.sales_items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

    def reserve_stock(self):
        """
        Reserve stock for pending orders
        Increases reserved_quantity in Stock model
        """
        if self.status == 'PENDING':
            for sales_item in self.sales_items.all():
                sales_item.reserve_stock()

    def release_reserved_stock(self):
        """
        Release reserved stock (e.g., when order is cancelled)
        Decreases reserved_quantity in Stock model
        """
        for sales_item in self.sales_items.all():
            sales_item.release_reserved_stock()

    def reduce_stock(self):
        """
        Reduce stock when order is shipped or delivered
        Decreases quantity and reserved_quantity in Stock model
        """
        if self.status in ['SHIPPED', 'DELIVERED']:
            for sales_item in self.sales_items.all():
                sales_item.reduce_stock()

    def mark_as_shipped(self):
        """Mark sales order as shipped and reduce stock"""
        if self.status not in ['SHIPPED', 'DELIVERED']:
            from django.utils import timezone
            self.status = 'SHIPPED'
            self.shipped_date = timezone.now().date()
            self.save(update_fields=['status', 'shipped_date'])
            self.reduce_stock()

    def mark_as_delivered(self):
        """Mark sales order as delivered"""
        if self.status != 'DELIVERED':
            from django.utils import timezone
            old_status = self.status
            self.status = 'DELIVERED'
            self.delivered_date = timezone.now().date()
            self.save(update_fields=['status', 'delivered_date'])
            # Reduce stock if not already shipped
            if old_status not in ['SHIPPED', 'DELIVERED']:
                self.reduce_stock()

    def cancel_order(self):
        """Cancel order and release reserved stock"""
        if self.status != 'CANCELLED':
            self.status = 'CANCELLED'
            self.save(update_fields=['status'])
            self.release_reserved_stock()

    def save(self, *args, **kwargs):
        """Override save to handle stock reservation"""
        # Get old status if updating
        if self.pk:
            old_instance = SalesOrder.objects.get(pk=self.pk)
            old_status = old_instance.status
        else:
            old_status = None

        super().save(*args, **kwargs)

        # Handle stock operations based on status changes
        if old_status != self.status:
            if self.status == 'PENDING' and old_status != 'PENDING':
                self.reserve_stock()
            elif self.status == 'CANCELLED' and old_status != 'CANCELLED':
                self.release_reserved_stock()
            elif self.status in ['SHIPPED', 'DELIVERED'] and old_status not in ['SHIPPED', 'DELIVERED']:
                self.reduce_stock()


class SalesItem(models.Model):
    """
    Sales Item model for individual items in a sales order
    Includes stock reduction logic
    """
    sales_order = models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE,
        related_name='sales_items',
        verbose_name=_("Sales Order"),
        help_text=_("Sales order this item belongs to")
    )
    item = models.ForeignKey(
        'inventory.Item',
        on_delete=models.PROTECT,
        related_name='sales_items',
        verbose_name=_("Item"),
        help_text=_("Product/item being sold")
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_("Quantity"),
        help_text=_("Quantity of items ordered")
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Unit Price"),
        help_text=_("Selling price per unit")
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Discount Percentage"),
        help_text=_("Discount percentage for this line item")
    )
    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        editable=False,
        verbose_name=_("Line Total"),
        help_text=_("Total amount for this line item")
    )
    shipped_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Shipped Quantity"),
        help_text=_("Quantity actually shipped")
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
        verbose_name = _("Sales Item")
        verbose_name_plural = _("Sales Items")
        ordering = ['sales_order', 'item']
        indexes = [
            models.Index(fields=['sales_order']),
            models.Index(fields=['item']),
        ]

    def __str__(self):
        return f"{self.sales_order.order_number} - {self.item.name} x{self.quantity}"

    def calculate_line_total(self):
        """Calculate line total with discount"""
        subtotal = self.quantity * self.unit_price
        discount_amount = subtotal * (self.discount_percentage / Decimal('100'))
        return subtotal - discount_amount

    def get_stock(self, warehouse=None):
        """
        Get stock for this item from the sales order's warehouse
        or from the first available warehouse
        """
        from inventory.models import Stock
        
        # Use order's warehouse if specified
        if warehouse:
            try:
                return Stock.objects.get(item=self.item, warehouse=warehouse)
            except Stock.DoesNotExist:
                pass
        
        # Try order's warehouse
        if self.sales_order.warehouse:
            try:
                return Stock.objects.get(
                    item=self.item, 
                    warehouse=self.sales_order.warehouse
                )
            except Stock.DoesNotExist:
                pass
        
        # Get first available stock
        stock = Stock.objects.filter(item=self.item).first()
        return stock

    def check_stock_availability(self, warehouse=None):
        """Check if sufficient stock is available"""
        stock = self.get_stock(warehouse)
        if not stock:
            return False, "Stock not found for this item"
        if stock.available_quantity < self.quantity:
            return False, f"Insufficient stock. Available: {stock.available_quantity}, Required: {self.quantity}"
        return True, "Stock available"

    def reserve_stock(self):
        """
        Reserve stock for this item
        Increases reserved_quantity in Stock model
        """
        stock = self.get_stock()
        if stock:
            stock.reserved_quantity += self.quantity
            stock.save(update_fields=['reserved_quantity'])

    def release_reserved_stock(self):
        """
        Release reserved stock for this item
        Decreases reserved_quantity in Stock model
        """
        stock = self.get_stock()
        if stock:
            stock.reserved_quantity = max(0, stock.reserved_quantity - self.quantity)
            stock.save(update_fields=['reserved_quantity'])

    def reduce_stock(self):
        """
        Reduce stock when order is shipped or delivered
        Decreases quantity and reserved_quantity in Stock model
        """
        stock = self.get_stock()
        if stock:
            with transaction.atomic():
                # Reduce reserved quantity first
                stock.reserved_quantity = max(0, stock.reserved_quantity - self.quantity)
                # Reduce actual quantity
                stock.quantity = max(0, stock.quantity - self.quantity)
                stock.save(update_fields=['quantity', 'reserved_quantity'])
                
                # Update shipped quantity
                self.shipped_quantity = self.quantity
                self.save(update_fields=['shipped_quantity'])

    def save(self, *args, **kwargs):
        """Override save to calculate line total and handle stock"""
        # Calculate line total
        self.line_total = self.calculate_line_total()
        
        super().save(*args, **kwargs)
        
        # Update sales order total
        if self.sales_order:
            self.sales_order.calculate_total()
            
        # Reserve stock if order is pending
        if self.sales_order.status == 'PENDING':
            self.reserve_stock()

    def delete(self, *args, **kwargs):
        """Override delete to release reserved stock"""
        # Release reserved stock before deleting
        if self.sales_order.status == 'PENDING':
            self.release_reserved_stock()
        super().delete(*args, **kwargs)
        # Update sales order total
        if self.sales_order:
            self.sales_order.calculate_total()

    def get_profit_margin(self):
        """Calculate profit margin for this line item"""
        if self.item.cost_price > 0:
            profit = self.unit_price - self.item.cost_price
            margin = (profit / self.item.cost_price) * 100
            return round(margin, 2)
        return 0

    def get_profit_amount(self):
        """Calculate total profit amount for this line item"""
        if self.item.cost_price > 0:
            profit_per_unit = self.unit_price - self.item.cost_price
            return profit_per_unit * Decimal(str(self.quantity))
        return Decimal('0.00')

