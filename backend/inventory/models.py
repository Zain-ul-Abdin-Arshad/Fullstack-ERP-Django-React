"""
Inventory Management Models
Models for managing products, stock levels, warehouses, and categories
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class Category(models.Model):
    """
    Product category model for organizing items
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Category Name"),
        help_text=_("Name of the product category")
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Category Code"),
        help_text=_("Short code for the category")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Detailed description of the category")
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name=_("Parent Category"),
        help_text=_("Parent category for hierarchical organization")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this category is currently active")
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
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name

    def get_full_path(self):
        """Return full category path including parent categories"""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name


class Warehouse(models.Model):
    """
    Warehouse/Location model for storing physical locations
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Warehouse Name"),
        help_text=_("Name of the warehouse or storage location")
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Warehouse Code"),
        help_text=_("Short code for the warehouse")
    )
    address = models.TextField(
        verbose_name=_("Address"),
        help_text=_("Physical address of the warehouse")
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_("City")
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("State/Province")
    )
    country = models.CharField(
        max_length=100,
        default="USA",
        verbose_name=_("Country")
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Postal Code")
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Phone Number")
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_("Email Address")
    )
    manager_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Manager Name")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this warehouse is currently active")
    )
    capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Capacity"),
        help_text=_("Total storage capacity (in square meters or cubic meters)")
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
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    Product/Item model representing car spare parts
    """
    UNIT_CHOICES = [
        ('PCS', 'Pieces'),
        ('BOX', 'Box'),
        ('PKG', 'Package'),
        ('SET', 'Set'),
        ('PAIR', 'Pair'),
        ('KG', 'Kilogram'),
        ('L', 'Liter'),
        ('M', 'Meter'),
    ]

    # Basic Information
    name = models.CharField(
        max_length=200,
        verbose_name=_("Item Name"),
        help_text=_("Name of the product/item")
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("SKU"),
        help_text=_("Stock Keeping Unit - unique identifier")
    )
    barcode = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("Barcode"),
        help_text=_("Barcode or UPC code")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Detailed description of the item")
    )

    # Relationships
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='items',
        verbose_name=_("Category"),
        help_text=_("Product category")
    )
    vendor = models.ForeignKey(
        'vendors.Vendor',
        on_delete=models.PROTECT,
        related_name='items',
        blank=True,
        null=True,
        verbose_name=_("Primary Vendor"),
        help_text=_("Primary supplier/vendor for this item")
    )

    # Pricing
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Cost Price"),
        help_text=_("Purchase cost per unit")
    )
    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Selling Price"),
        help_text=_("Retail selling price per unit")
    )

    # Unit Information
    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='PCS',
        verbose_name=_("Unit of Measurement"),
        help_text=_("Unit of measurement for this item")
    )
    reorder_level = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Reorder Level"),
        help_text=_("Minimum stock level before reordering")
    )
    reorder_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Reorder Quantity"),
        help_text=_("Standard quantity to reorder")
    )

    # Physical Attributes
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Weight (kg)"),
        help_text=_("Weight per unit in kilograms")
    )
    dimensions = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Dimensions"),
        help_text=_("Dimensions (L x W x H)")
    )

    # Vehicle Compatibility (for car spare parts)
    vehicle_make = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Vehicle Make"),
        help_text=_("Compatible vehicle manufacturer")
    )
    vehicle_model = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Vehicle Model"),
        help_text=_("Compatible vehicle model")
    )
    vehicle_year_from = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        verbose_name=_("Vehicle Year From"),
        help_text=_("Earliest compatible vehicle year")
    )
    vehicle_year_to = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        verbose_name=_("Vehicle Year To"),
        help_text=_("Latest compatible vehicle year")
    )

    # Status and Flags
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this item is currently active")
    )
    is_trackable = models.BooleanField(
        default=True,
        verbose_name=_("Is Trackable"),
        help_text=_("Whether stock levels should be tracked for this item")
    )
    allow_backorder = models.BooleanField(
        default=False,
        verbose_name=_("Allow Backorder"),
        help_text=_("Whether backorders are allowed when out of stock")
    )

    # Images and Documents
    image = models.ImageField(
        upload_to='items/images/',
        blank=True,
        null=True,
        verbose_name=_("Item Image")
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
        ordering = ['name']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['barcode']),
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['vendor']),
            models.Index(fields=['is_active']),
            models.Index(fields=['vehicle_make', 'vehicle_model']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_total_stock(self):
        """Calculate total stock across all warehouses"""
        return self.stock_items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

    def is_low_stock(self):
        """Check if item is below reorder level"""
        total_stock = self.get_total_stock()
        return total_stock <= self.reorder_level

    def get_margin(self):
        """Calculate profit margin percentage"""
        if self.cost_price > 0:
            margin = ((self.selling_price - self.cost_price) / self.cost_price) * 100
            return round(margin, 2)
        return 0


class Stock(models.Model):
    """
    Stock model tracking inventory levels per item per warehouse
    """
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='stock_items',
        verbose_name=_("Item"),
        help_text=_("Product/item")
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='stock_items',
        verbose_name=_("Warehouse"),
        help_text=_("Warehouse location")
    )
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Quantity"),
        help_text=_("Current stock quantity")
    )
    reserved_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Reserved Quantity"),
        help_text=_("Quantity reserved for pending orders")
    )
    available_quantity = models.IntegerField(
        default=0,
        editable=False,
        verbose_name=_("Available Quantity"),
        help_text=_("Available quantity (quantity - reserved)")
    )
    min_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Minimum Quantity"),
        help_text=_("Minimum stock level for this warehouse")
    )
    max_quantity = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name=_("Maximum Quantity"),
        help_text=_("Maximum stock level for this warehouse")
    )
    average_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_("Average Cost"),
        help_text=_("Average cost per unit for this stock")
    )
    last_restocked = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Last Restocked"),
        help_text=_("Date and time of last restocking")
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
        verbose_name = _("Stock")
        verbose_name_plural = _("Stock")
        unique_together = [['item', 'warehouse']]
        ordering = ['item', 'warehouse']
        indexes = [
            models.Index(fields=['item', 'warehouse']),
            models.Index(fields=['quantity']),
            models.Index(fields=['warehouse']),
        ]

    def __str__(self):
        return f"{self.item.name} - {self.warehouse.name}: {self.quantity}"

    def save(self, *args, **kwargs):
        """Override save to calculate available quantity"""
        self.available_quantity = max(0, self.quantity - self.reserved_quantity)
        super().save(*args, **kwargs)

    def is_low_stock(self):
        """Check if stock is below minimum level"""
        return self.quantity <= self.min_quantity

    def is_out_of_stock(self):
        """Check if stock is out"""
        return self.quantity == 0

    def can_fulfill_order(self, requested_quantity):
        """Check if stock can fulfill requested quantity"""
        return self.available_quantity >= requested_quantity


class StockAlert(models.Model):
    """
    Stock Alert model for tracking low stock alerts per warehouse
    """
    ALERT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACKNOWLEDGED', 'Acknowledged'),
        ('RESOLVED', 'Resolved'),
    ]

    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name='alerts',
        verbose_name=_("Stock"),
        help_text=_("Stock entry that triggered the alert")
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='stock_alerts',
        verbose_name=_("Warehouse"),
        help_text=_("Warehouse where the alert occurred")
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='stock_alerts',
        verbose_name=_("Item"),
        help_text=_("Item that triggered the alert")
    )
    current_quantity = models.IntegerField(
        verbose_name=_("Current Quantity"),
        help_text=_("Stock quantity when alert was created")
    )
    min_quantity = models.IntegerField(
        verbose_name=_("Minimum Quantity"),
        help_text=_("Minimum required quantity")
    )
    alert_status = models.CharField(
        max_length=20,
        choices=ALERT_STATUS_CHOICES,
        default='PENDING',
        verbose_name=_("Alert Status"),
        help_text=_("Status of the alert")
    )
    message = models.TextField(
        verbose_name=_("Alert Message"),
        help_text=_("Alert message")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    acknowledged_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Acknowledged At")
    )
    resolved_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Resolved At")
    )

    class Meta:
        verbose_name = _("Stock Alert")
        verbose_name_plural = _("Stock Alerts")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['warehouse']),
            models.Index(fields=['item']),
            models.Index(fields=['alert_status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Low Stock Alert: {self.item.name} - {self.warehouse.name} ({self.current_quantity}/{self.min_quantity})"

    @classmethod
    def create_alert(cls, stock):
        """
        Create a stock alert if one doesn't already exist for this stock
        
        Args:
            stock: Stock instance
            
        Returns:
            StockAlert instance or None if alert already exists
        """
        # Check if there's already a pending alert for this stock
        existing_alert = cls.objects.filter(
            stock=stock,
            alert_status='PENDING'
        ).first()
        
        if existing_alert:
            # Update existing alert if quantity changed
            if existing_alert.current_quantity != stock.quantity:
                existing_alert.current_quantity = stock.quantity
                existing_alert.message = (
                    f"Low stock alert for {stock.item.name} in {stock.warehouse.name}. "
                    f"Current quantity: {stock.quantity}, Minimum required: {stock.min_quantity}"
                )
                existing_alert.save()
            return existing_alert
        
        # Create new alert
        alert = cls.objects.create(
            stock=stock,
            warehouse=stock.warehouse,
            item=stock.item,
            current_quantity=stock.quantity,
            min_quantity=stock.min_quantity,
            alert_status='PENDING',
            message=(
                f"Low stock alert for {stock.item.name} in {stock.warehouse.name}. "
                f"Current quantity: {stock.quantity}, Minimum required: {stock.min_quantity}"
            )
        )
        
        # Send alert notification (can be extended to email, SMS, etc.)
        send_stock_alert_notification(alert)
        
        return alert

    def acknowledge(self):
        """Mark alert as acknowledged"""
        from django.utils import timezone
        self.alert_status = 'ACKNOWLEDGED'
        self.acknowledged_at = timezone.now()
        self.save(update_fields=['alert_status', 'acknowledged_at'])

    def resolve(self):
        """Mark alert as resolved"""
        from django.utils import timezone
        self.alert_status = 'RESOLVED'
        self.resolved_at = timezone.now()
        self.save(update_fields=['alert_status', 'resolved_at'])

    def is_resolved(self):
        """Check if stock issue is resolved"""
        return self.stock.quantity > self.stock.min_quantity


def send_stock_alert_notification(alert):
    """
    Send stock alert notification
    
    This function can be extended to send:
    - Email notifications
    - SMS alerts
    - Push notifications
    - Slack/Discord messages
    - etc.
    
    Args:
        alert: StockAlert instance
    """
    # Log the alert (can be extended to actual notification system)
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(
        f"LOW STOCK ALERT: {alert.item.name} in {alert.warehouse.name} - "
        f"Current: {alert.current_quantity}, Minimum: {alert.min_quantity}"
    )
    
    # TODO: Implement actual notification sending
    # Example: Send email to warehouse manager
    # Example: Send SMS alert
    # Example: Create notification in notification system

