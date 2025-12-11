"""
Django signals for Sales module
Handles automatic stock reduction and validation when sales items are created
"""

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import models
from .models import SalesItem, SalesOrder
from inventory.models import Stock


@receiver(pre_save, sender=SalesItem)
def validate_stock_before_sale(sender, instance, **kwargs):
    """
    Validate sufficient stock before creating/updating SalesItem
    
    Raises ValidationError if insufficient stock available
    """
    # Skip validation if this is an update and quantity hasn't changed
    if instance.pk:
        try:
            old_instance = SalesItem.objects.get(pk=instance.pk)
            if old_instance.quantity == instance.quantity and \
               old_instance.sales_order.status == instance.sales_order.status:
                return
        except SalesItem.DoesNotExist:
            pass
    
    # Only validate for PENDING, CONFIRMED, SHIPPED, DELIVERED statuses
    if instance.sales_order.status in ['PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED']:
        validate_stock_availability(instance)


def validate_stock_availability(sales_item):
    """
    Validate that sufficient stock is available for the sales item
    
    Args:
        sales_item: SalesItem instance
        
    Raises:
        ValidationError: If insufficient stock
    """
    item = sales_item.item
    sales_order = sales_item.sales_order
    requested_quantity = sales_item.quantity
    
    # Get warehouse from sales order
    warehouse = sales_order.warehouse
    
    # If no warehouse specified, try to find stock in any warehouse
    if warehouse:
        try:
            stock = Stock.objects.get(item=item, warehouse=warehouse)
            available_qty = stock.available_quantity
        except Stock.DoesNotExist:
            raise ValidationError(
                f"Insufficient stock: No stock found for item '{item.name}' "
                f"in warehouse '{warehouse.name}'"
            )
    else:
        # Check total available stock across all warehouses
        total_stock = Stock.objects.filter(item=item).aggregate(
            total=models.Sum('available_quantity')
        )['total'] or 0
        
        if total_stock < requested_quantity:
            raise ValidationError(
                f"Insufficient stock: Only {total_stock} units available "
                f"for item '{item.name}', but {requested_quantity} requested"
            )
        return
    
    # Validate available quantity
    if available_qty < requested_quantity:
        raise ValidationError(
            f"Insufficient stock: Only {available_qty} units available "
            f"for item '{item.name}' in warehouse '{warehouse.name}', "
            f"but {requested_quantity} requested"
        )


@receiver(post_save, sender=SalesItem)
def decrease_stock_on_sale(sender, instance, created, **kwargs):
    """
    Automatically decrease stock when SalesItem is created/updated
    
    Stock is decreased when:
    - Sales order status is SHIPPED or DELIVERED
    - Stock is physically reduced
    """
    sales_order = instance.sales_order
    
    # Only decrease stock if order is shipped or delivered
    if sales_order.status in ['SHIPPED', 'DELIVERED']:
        decrease_stock_from_sales_item(instance)


@receiver(post_save, sender=SalesOrder)
def update_stock_on_order_status_change(sender, instance, created, **kwargs):
    """
    Update stock when sales order status changes to SHIPPED or DELIVERED
    """
    if instance.status in ['SHIPPED', 'DELIVERED']:
        # Decrease stock for all sales items
        for sales_item in instance.sales_items.all():
            decrease_stock_from_sales_item(sales_item)


def decrease_stock_from_sales_item(sales_item):
    """
    Decrease stock quantity based on sales item
    
    Args:
        sales_item: SalesItem instance
    """
    item = sales_item.item
    sales_order = sales_item.sales_order
    quantity = sales_item.quantity
    
    if quantity <= 0:
        return
    
    # Get warehouse from sales order
    warehouse = sales_order.warehouse
    
    if not warehouse:
        # Try to find stock in any warehouse
        stock = Stock.objects.filter(item=item).first()
        if not stock:
            raise ValidationError(
                f"No stock found for item '{item.name}'"
            )
        warehouse = stock.warehouse
    
    # Get stock entry
    try:
        stock = Stock.objects.get(item=item, warehouse=warehouse)
    except Stock.DoesNotExist:
        raise ValidationError(
            f"No stock found for item '{item.name}' in warehouse '{warehouse.name}'"
        )
    
    # Validate sufficient stock
    if stock.available_quantity < quantity:
        raise ValidationError(
            f"Insufficient stock: Only {stock.available_quantity} units available, "
            f"but {quantity} requested"
        )
    
    # Update stock with transaction safety
    with transaction.atomic():
        # Reduce reserved quantity first (if it was reserved)
        if stock.reserved_quantity >= quantity:
            stock.reserved_quantity -= quantity
        else:
            # If reserved quantity is less, reduce it to 0 and reduce from actual quantity
            remaining = quantity - stock.reserved_quantity
            stock.reserved_quantity = 0
            stock.quantity -= remaining
        
        # Reduce actual quantity
        stock.quantity = max(0, stock.quantity - quantity)
        
        # Update shipped quantity
        sales_item.shipped_quantity = quantity
        sales_item.save(update_fields=['shipped_quantity'])
        
        # Save stock
        stock.save()
        
        # Check for low stock alert
        check_and_send_low_stock_alert(stock)


def check_and_send_low_stock_alert(stock):
    """
    Check if stock is low and send alert if needed
    
    Args:
        stock: Stock instance
    """
    if stock.is_low_stock():
        from inventory.models import StockAlert
        StockAlert.create_alert(stock)

