"""
Django REST Framework Serializers for Purchases module
"""

from rest_framework import serializers
from .models import PurchaseOrder, PurchaseItem


class PurchaseItemSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseItem model"""
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    cost_breakdown = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseItem
        fields = [
            'id', 'purchase_order', 'item', 'item_name', 'item_sku',
            'quantity', 'unit_cost', 'freight_cost', 'customs_duty',
            'other_costs', 'line_total', 'landed_cost_per_unit',
            'total_landed_cost', 'received_quantity', 'cost_breakdown',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'line_total', 'landed_cost_per_unit', 'total_landed_cost',
            'created_at', 'updated_at', 'cost_breakdown'
        ]

    def get_cost_breakdown(self, obj):
        """Get detailed cost breakdown"""
        return obj.get_cost_breakdown()


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseOrder model"""
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    vendor_code = serializers.CharField(source='vendor.code', read_only=True)
    purchase_items = PurchaseItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'vendor', 'vendor_name', 'vendor_code', 'order_number',
            'order_date', 'expected_delivery_date', 'received_date',
            'total_amount', 'status', 'notes', 'purchase_items',
            'item_count', 'total_quantity', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'total_amount', 'received_date', 'created_at', 'updated_at',
            'item_count', 'total_quantity'
        ]

    def get_item_count(self, obj):
        """Get number of items in order"""
        return obj.get_item_count()

    def get_total_quantity(self, obj):
        """Get total quantity"""
        return obj.get_total_quantity()


class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating PurchaseOrder with items"""
    purchase_items = PurchaseItemSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            'vendor', 'order_number', 'order_date', 'expected_delivery_date',
            'status', 'notes', 'purchase_items'
        ]

    def create(self, validated_data):
        """Create purchase order with items"""
        items_data = validated_data.pop('purchase_items')
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        
        for item_data in items_data:
            PurchaseItem.objects.create(purchase_order=purchase_order, **item_data)
        
        purchase_order.calculate_total()
        return purchase_order

