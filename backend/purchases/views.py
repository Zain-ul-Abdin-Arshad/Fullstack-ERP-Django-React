"""
Django REST Framework Viewsets for Purchases module
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import PurchaseOrder, PurchaseItem
from .serializers import (
    PurchaseOrderSerializer, PurchaseItemSerializer,
    PurchaseOrderCreateSerializer
)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """ViewSet for PurchaseOrder model"""
    queryset = PurchaseOrder.objects.select_related('vendor').prefetch_related('purchase_items').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'vendor', 'order_date']
    search_fields = ['order_number', 'vendor__name', 'notes']
    ordering_fields = ['order_date', 'created_at', 'total_amount']
    ordering = ['-order_date', '-created_at']

    def get_serializer_class(self):
        """Use different serializer for create"""
        if self.action == 'create':
            return PurchaseOrderCreateSerializer
        return PurchaseOrderSerializer

    @action(detail=True, methods=['post'])
    def mark_received(self, request, pk=None):
        """Mark purchase order as received"""
        purchase_order = self.get_object()
        purchase_order.mark_as_received()
        serializer = self.get_serializer(purchase_order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def recalculate_total(self, request, pk=None):
        """Recalculate purchase order total"""
        purchase_order = self.get_object()
        total = purchase_order.calculate_total()
        serializer = self.get_serializer(purchase_order)
        return Response({
            'total_amount': total,
            'purchase_order': serializer.data
        })


class PurchaseItemViewSet(viewsets.ModelViewSet):
    """ViewSet for PurchaseItem model"""
    queryset = PurchaseItem.objects.select_related('purchase_order', 'item').all()
    serializer_class = PurchaseItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['purchase_order', 'item', 'purchase_order__status']
    search_fields = ['item__name', 'item__sku', 'purchase_order__order_number']
    ordering_fields = ['purchase_order', 'item', 'created_at']
    ordering = ['purchase_order', 'item']

