"""
Django REST Framework Viewsets for Inventory module
"""

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Warehouse, Item, Stock
from .serializers import (
    CategorySerializer, WarehouseSerializer,
    ItemSerializer, StockSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Category model"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'parent']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        """Get subcategories of a category"""
        category = self.get_object()
        subcategories = category.subcategories.all()
        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data)


class WarehouseViewSet(viewsets.ModelViewSet):
    """ViewSet for Warehouse model"""
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'country', 'city']
    search_fields = ['name', 'code', 'address', 'city', 'manager_name']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']


class ItemViewSet(viewsets.ModelViewSet):
    """ViewSet for Item model"""
    queryset = Item.objects.select_related('category', 'vendor').all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'is_active', 'is_trackable', 'category', 'vendor',
        'vehicle_make', 'vehicle_model', 'unit'
    ]
    search_fields = [
        'name', 'sku', 'barcode', 'description',
        'vehicle_make', 'vehicle_model'
    ]
    ordering_fields = ['name', 'sku', 'created_at', 'selling_price']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def stock(self, request, pk=None):
        """Get stock levels for an item across all warehouses"""
        item = self.get_object()
        stock_items = item.stock_items.select_related('warehouse').all()
        serializer = StockSerializer(stock_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get items that are low on stock"""
        items = [item for item in self.get_queryset() if item.is_low_stock()]
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)


class StockViewSet(viewsets.ModelViewSet):
    """ViewSet for Stock model"""
    queryset = Stock.objects.select_related('item', 'warehouse').all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['item', 'warehouse', 'item__category']
    search_fields = ['item__name', 'item__sku', 'warehouse__name']
    ordering_fields = ['item__name', 'quantity', 'created_at']
    ordering = ['item', 'warehouse']

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get stock items that are low on stock"""
        stock_items = [stock for stock in self.get_queryset() if stock.is_low_stock()]
        serializer = self.get_serializer(stock_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """Get stock items that are out of stock"""
        stock_items = [stock for stock in self.get_queryset() if stock.is_out_of_stock()]
        serializer = self.get_serializer(stock_items, many=True)
        return Response(serializer.data)

