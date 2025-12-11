"""
Django REST Framework Serializers for Sales module
"""

from rest_framework import serializers
from .models import SalesOrder, SalesItem


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

