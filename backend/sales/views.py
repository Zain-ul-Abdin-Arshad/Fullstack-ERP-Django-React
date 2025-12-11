"""
Django REST Framework Viewsets for Sales module
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import SalesOrder, SalesItem
from .serializers import (
    SalesOrderSerializer, SalesItemSerializer,
    SalesOrderCreateSerializer
)


class SalesOrderViewSet(viewsets.ModelViewSet):
    """ViewSet for SalesOrder model"""
    queryset = SalesOrder.objects.select_related('client', 'warehouse').prefetch_related('sales_items').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'client', 'warehouse', 'order_date']
    search_fields = ['order_number', 'client__name', 'notes']
    ordering_fields = ['order_date', 'created_at', 'total_amount']
    ordering = ['-order_date', '-created_at']

    def get_serializer_class(self):
        """Use different serializer for create"""
        if self.action == 'create':
            return SalesOrderCreateSerializer
        return SalesOrderSerializer

    @action(detail=True, methods=['post'])
    def mark_shipped(self, request, pk=None):
        """Mark sales order as shipped"""
        sales_order = self.get_object()
        sales_order.mark_as_shipped()
        serializer = self.get_serializer(sales_order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_delivered(self, request, pk=None):
        """Mark sales order as delivered"""
        sales_order = self.get_object()
        sales_order.mark_as_delivered()
        serializer = self.get_serializer(sales_order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel sales order"""
        sales_order = self.get_object()
        sales_order.cancel_order()
        serializer = self.get_serializer(sales_order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def recalculate_total(self, request, pk=None):
        """Recalculate sales order total"""
        sales_order = self.get_object()
        total = sales_order.calculate_total()
        serializer = self.get_serializer(sales_order)
        return Response({
            'total_amount': total,
            'sales_order': serializer.data
        })


class SalesItemViewSet(viewsets.ModelViewSet):
    """ViewSet for SalesItem model"""
    queryset = SalesItem.objects.select_related('sales_order', 'item').all()
    serializer_class = SalesItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sales_order', 'item', 'sales_order__status']
    search_fields = ['item__name', 'item__sku', 'sales_order__order_number']
    ordering_fields = ['sales_order', 'item', 'created_at']
    ordering = ['sales_order', 'item']

