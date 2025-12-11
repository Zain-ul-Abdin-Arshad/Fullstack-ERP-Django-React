"""
Django REST Framework Serializers for Inventory module
"""

from rest_framework import serializers
from .models import Category, Warehouse, Item, Stock


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    subcategories_count = serializers.SerializerMethodField()
    full_path = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'code', 'description', 'parent', 'parent_name',
            'is_active', 'subcategories_count', 'full_path',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_subcategories_count(self, obj):
        """Get count of subcategories"""
        return obj.subcategories.count()

    def get_full_path(self, obj):
        """Get full category path"""
        return obj.get_full_path()


class WarehouseSerializer(serializers.ModelSerializer):
    """Serializer for Warehouse model"""
    full_address = serializers.SerializerMethodField()

    class Meta:
        model = Warehouse
        fields = [
            'id', 'name', 'code', 'address', 'city', 'state', 'country',
            'postal_code', 'phone', 'email', 'manager_name', 'is_active',
            'capacity', 'full_address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_full_address(self, obj):
        """Get formatted full address"""
        parts = [obj.address, obj.city, obj.state, obj.postal_code, obj.country]
        return ", ".join(filter(None, parts))


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item model"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_code = serializers.CharField(source='category.code', read_only=True)
    vendor_name = serializers.CharField(source='vendor.name', read_only=True, allow_null=True)
    total_stock = serializers.SerializerMethodField()
    is_low_stock = serializers.SerializerMethodField()
    margin = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'sku', 'barcode', 'description', 'category', 'category_name',
            'category_code', 'vendor', 'vendor_name', 'cost_price', 'selling_price',
            'unit', 'reorder_level', 'reorder_quantity', 'weight', 'dimensions',
            'vehicle_make', 'vehicle_model', 'vehicle_year_from', 'vehicle_year_to',
            'is_active', 'is_trackable', 'allow_backorder', 'image', 'total_stock',
            'is_low_stock', 'margin', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'total_stock', 'is_low_stock', 'margin']

    def get_total_stock(self, obj):
        """Get total stock across all warehouses"""
        return obj.get_total_stock()

    def get_is_low_stock(self, obj):
        """Check if item is low stock"""
        return obj.is_low_stock()

    def get_margin(self, obj):
        """Get profit margin percentage"""
        return obj.get_margin()


class StockSerializer(serializers.ModelSerializer):
    """Serializer for Stock model"""
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    warehouse_code = serializers.CharField(source='warehouse.code', read_only=True)
    is_low_stock = serializers.SerializerMethodField()
    is_out_of_stock = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = [
            'id', 'item', 'item_name', 'item_sku', 'warehouse', 'warehouse_name',
            'warehouse_code', 'quantity', 'reserved_quantity', 'available_quantity',
            'min_quantity', 'max_quantity', 'average_cost', 'last_restocked',
            'is_low_stock', 'is_out_of_stock', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'available_quantity', 'created_at', 'updated_at',
            'is_low_stock', 'is_out_of_stock'
        ]

    def get_is_low_stock(self, obj):
        """Check if stock is low"""
        return obj.is_low_stock()

    def get_is_out_of_stock(self, obj):
        """Check if stock is out"""
        return obj.is_out_of_stock()

