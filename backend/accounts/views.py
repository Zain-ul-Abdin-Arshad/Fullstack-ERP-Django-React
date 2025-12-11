"""
Django REST Framework Viewsets for Accounts module
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import date, timedelta
from .models import Payment, LedgerEntry, ProfitLoss
from .serializers import (
    PaymentSerializer, LedgerEntrySerializer, ProfitLossSerializer
)


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Payment model"""
    queryset = Payment.objects.select_related('vendor', 'client', 'purchase_order', 'sales_order').all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_type', 'payment_method', 'vendor', 'client', 'date', 'is_reconciled']
    search_fields = ['description', 'reference_number', 'vendor__name', 'client__name']
    ordering_fields = ['date', 'created_at', 'amount']
    ordering = ['-date', '-created_at']

    @action(detail=True, methods=['post'])
    def reconcile(self, request, pk=None):
        """Mark payment as reconciled"""
        payment = self.get_object()
        payment.is_reconciled = True
        payment.save()
        serializer = self.get_serializer(payment)
        return Response(serializer.data)


class LedgerEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for LedgerEntry model (read-only)"""
    queryset = LedgerEntry.objects.select_related('payment').all()
    serializer_class = LedgerEntrySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['entry_type', 'reference_type', 'date']
    search_fields = ['description']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date', '-created_at']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get ledger summary for date range"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date', str(date.today()))
        
        if not start_date:
            start_date = str(date.today().replace(day=1))
        
        total_debits = LedgerEntry.get_total_debits(start_date, end_date)
        total_credits = LedgerEntry.get_total_credits(start_date, end_date)
        balance = LedgerEntry.get_balance(start_date, end_date)
        
        return Response({
            'start_date': start_date,
            'end_date': end_date,
            'total_debits': float(total_debits),
            'total_credits': float(total_credits),
            'balance': float(balance)
        })


class ProfitLossViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ProfitLoss model (read-only)"""
    queryset = ProfitLoss.objects.all()
    serializer_class = ProfitLossSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['period_start', 'period_end']
    ordering_fields = ['period_end']
    ordering = ['-period_end']

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Calculate profit/loss for date range"""
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date', str(date.today()))
        
        if not start_date:
            return Response(
                {'error': 'start_date is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        p_l_data = ProfitLoss.calculate_profit_loss(start_date, end_date)
        
        return Response({
            'start_date': start_date,
            'end_date': end_date,
            **{k: float(v) for k, v in p_l_data.items()}
        })

    @action(detail=False, methods=['post'])
    def create_report(self, request):
        """Create and save profit/loss report"""
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date', str(date.today()))
        
        if not start_date:
            return Response(
                {'error': 'start_date is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        report = ProfitLoss.create_report(start_date, end_date)
        serializer = self.get_serializer(report)
        return Response(serializer.data)

