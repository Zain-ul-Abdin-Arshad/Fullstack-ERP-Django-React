"""
Django REST Framework Serializers for Sales module
"""

from rest_framework import serializers
from .models import SalesOrder, SalesItem
from decimal import Decimal


class SalesItemSerializer(serializers.ModelSerializer):
    """Serializer for SalesItem model"""
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    profit_margin = serializers.SerializerMethodField()
    profit_amount = serializers.SerializerMethodField()

    class Meta:
        model = SalesItem
        fields = [
            'id', 'sales_order', 'item', 'item_name', 'item_sku',
            'quantity', 'unit_price', 'discount_percentage', 'line_total',
            'shipped_quantity', 'profit_margin', 'profit_amount',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'line_total', 'created_at', 'updated_at',
            'profit_margin', 'profit_amount'
        ]

    def get_profit_margin(self, obj):
        """Get profit margin percentage"""
        return obj.get_profit_margin()

    def get_profit_amount(self, obj):
        """Get total profit amount"""
        return float(obj.get_profit_amount())


class SalesOrderSerializer(serializers.ModelSerializer):
    """Serializer for SalesOrder model"""
    client_name = serializers.CharField(source='client.name', read_only=True)
    client_code = serializers.CharField(source='client.code', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True, allow_null=True)
    sales_items = SalesItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'client', 'client_name', 'client_code', 'order_number',
            'order_date', 'expected_delivery_date', 'shipped_date',
            'delivered_date', 'total_amount', 'discount_amount', 'status',
            'warehouse', 'warehouse_name', 'notes', 'sales_items',
            'item_count', 'total_quantity', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'total_amount', 'shipped_date', 'delivered_date',
            'created_at', 'updated_at', 'item_count', 'total_quantity'
        ]

    def get_item_count(self, obj):
        """Get number of items in order"""
        return obj.get_item_count()

    def get_total_quantity(self, obj):
        """Get total quantity"""
        return obj.get_total_quantity()


class SalesOrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating SalesOrder with items"""
    sales_items = SalesItemSerializer(many=True)

    class Meta:
        model = SalesOrder
        fields = [
            'client', 'order_number', 'order_date', 'expected_delivery_date',
            'status', 'warehouse', 'discount_amount', 'notes', 'sales_items'
        ]

    def create(self, validated_data):
        """Create sales order with items"""
        items_data = validated_data.pop('sales_items')
        sales_order = SalesOrder.objects.create(**validated_data)
        
        for item_data in items_data:
            SalesItem.objects.create(sales_order=sales_order, **item_data)
        
        sales_order.calculate_total()
        return sales_order


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for generating invoices/bills from sales orders"""
    client_name = serializers.CharField(source='client.name', read_only=True)
    client_code = serializers.CharField(source='client.code', read_only=True)
    client_address = serializers.SerializerMethodField()
    client_contact = serializers.SerializerMethodField()
    client_email = serializers.CharField(source='client.email', read_only=True)
    client_tax_id = serializers.CharField(source='client.tax_id', read_only=True, allow_null=True)
    invoice_number = serializers.CharField(source='order_number', read_only=True)
    invoice_date = serializers.DateField(source='order_date', read_only=True)
    items = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    discount = serializers.DecimalField(source='discount_amount', max_digits=12, decimal_places=2, read_only=True)
    total = serializers.DecimalField(source='total_amount', max_digits=12, decimal_places=2, read_only=True)
    status_display = serializers.SerializerMethodField()
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True, allow_null=True)
    notes = serializers.CharField(read_only=True, allow_null=True)

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'invoice_number', 'invoice_date', 'status', 'status_display',
            'client_name', 'client_code', 'client_address', 'client_contact',
            'client_email', 'client_tax_id', 'warehouse_name',
            'items', 'subtotal', 'discount', 'total', 'notes',
            'expected_delivery_date', 'shipped_date', 'delivered_date'
        ]

    def get_client_address(self, obj):
        """Get formatted client address"""
        client = obj.client
        address_parts = []
        if client.address:
            address_parts.append(client.address)
        if client.city:
            address_parts.append(client.city)
        if client.state:
            address_parts.append(client.state)
        if client.postal_code:
            address_parts.append(client.postal_code)
        if client.country:
            address_parts.append(client.country)
        return ', '.join(address_parts) if address_parts else 'N/A'

    def get_client_contact(self, obj):
        """Get formatted client contact information"""
        client = obj.client
        contact_parts = []
        if client.contact_number:
            contact_parts.append(f"Phone: {client.contact_number}")
        if client.email:
            contact_parts.append(f"Email: {client.email}")
        return ' | '.join(contact_parts) if contact_parts else 'N/A'

    def get_items(self, obj):
        """Get invoice items with details"""
        items = []
        for sales_item in obj.sales_items.all():
            items.append({
                'id': sales_item.id,
                'item_name': sales_item.item.name,
                'item_sku': sales_item.item.sku,
                'description': sales_item.item.description or '',
                'quantity': sales_item.quantity,
                'unit_price': float(sales_item.unit_price),
                'discount_percentage': float(sales_item.discount_percentage),
                'line_total': float(sales_item.line_total),
            })
        return items

    def get_subtotal(self, obj):
        """Calculate subtotal before discount"""
        subtotal = sum(item.line_total for item in obj.sales_items.all())
        return float(subtotal + obj.discount_amount)

    def get_status_display(self, obj):
        """Get human-readable status"""
        return obj.get_status_display()

