"""
Django signals for Purchase module
Handles automatic stock updates when purchase items are received
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from .models import PurchaseItem, PurchaseOrder
from inventory.models import Stock, Warehouse


@receiver(post_save, sender=PurchaseItem)
def update_stock_on_purchase_received(sender, instance, created, **kwargs):
    """
    Automatically increase stock when PurchaseItem is received
    
    Stock is increased when:
    - Purchase order status is RECEIVED
    - received_quantity > 0
    """
    purchase_order = instance.purchase_order
    
    # Only update stock if order is received
    if purchase_order.status == 'RECEIVED' and instance.received_quantity > 0:
        increase_stock_from_purchase_item(instance)


@receiver(post_save, sender=PurchaseOrder)
def update_stock_on_order_received(sender, instance, created, **kwargs):
    """
    Update stock for all items when purchase order status changes to RECEIVED
    """
    if instance.status == 'RECEIVED':
        # Update stock for all purchase items
        for purchase_item in instance.purchase_items.all():
            if purchase_item.received_quantity > 0:
                increase_stock_from_purchase_item(purchase_item)


def increase_stock_from_purchase_item(purchase_item):
    """
    Increase stock quantity based on purchase item
    
    Args:
        purchase_item: PurchaseItem instance
    """
    item = purchase_item.item
    purchase_order = purchase_item.purchase_order
    received_qty = purchase_item.received_quantity
    
    if received_qty <= 0:
        return
    
    # Determine warehouse
    # Get first active warehouse or create default
    warehouse = Warehouse.objects.filter(is_active=True).first()
    if not warehouse:
        # Create default warehouse if none exists
        warehouse = Warehouse.objects.create(
            name="Default Warehouse",
            code="WH-DEFAULT",
            address="Default Address",
            city="Default City",
            country="Default Country",
            is_active=True
        )
    
    if not warehouse:
        return
    
    # Get or create stock entry
    stock, created = Stock.objects.get_or_create(
        item=item,
        warehouse=warehouse,
        defaults={
            'quantity': 0,
            'reserved_quantity': 0,
            'average_cost': purchase_item.landed_cost_per_unit,
        }
    )
    
    # Update stock with transaction safety
    with transaction.atomic():
        # Calculate new average cost (weighted average)
        if stock.quantity > 0:
            total_cost = (stock.quantity * stock.average_cost) + \
                        (received_qty * purchase_item.landed_cost_per_unit)
            total_quantity = stock.quantity + received_qty
            stock.average_cost = total_cost / total_quantity if total_quantity > 0 else Decimal('0.00')
        else:
            stock.average_cost = purchase_item.landed_cost_per_unit
        
        # Increase quantity
        stock.quantity += received_qty
        
        # Update last restocked timestamp
        stock.last_restocked = timezone.now()
        
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

