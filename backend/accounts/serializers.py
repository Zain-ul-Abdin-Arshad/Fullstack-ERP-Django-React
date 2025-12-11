"""
Django REST Framework Serializers for Accounts module
"""

from rest_framework import serializers
from .models import Payment, LedgerEntry, ProfitLoss


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""
    vendor_name = serializers.CharField(source='vendor.name', read_only=True, allow_null=True)
    client_name = serializers.CharField(source='client.name', read_only=True, allow_null=True)
    party_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id', 'vendor', 'vendor_name', 'client', 'client_name',
            'party_name', 'amount', 'payment_type', 'payment_method',
            'date', 'description', 'reference_number', 'purchase_order',
            'sales_order', 'is_reconciled', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_party_name(self, obj):
        """Get vendor or client name"""
        if obj.vendor:
            return obj.vendor.name
        elif obj.client:
            return obj.client.name
        return None

    def validate(self, data):
        """Validate that either vendor or client is specified"""
        vendor = data.get('vendor')
        client = data.get('client')
        
        if not vendor and not client:
            raise serializers.ValidationError(
                "Either vendor or client must be specified."
            )
        if vendor and client:
            raise serializers.ValidationError(
                "Payment cannot be for both vendor and client."
            )
        return data


class LedgerEntrySerializer(serializers.ModelSerializer):
    """Serializer for LedgerEntry model"""
    balance = serializers.SerializerMethodField()

    class Meta:
        model = LedgerEntry
        fields = [
            'id', 'payment', 'date', 'description', 'debit_amount',
            'credit_amount', 'entry_type', 'reference_type', 'reference_id',
            'balance', 'created_at'
        ]
        read_only_fields = ['created_at', 'balance']

    def get_balance(self, obj):
        """Calculate balance for this entry"""
        return float(obj.credit_amount - obj.debit_amount)


class ProfitLossSerializer(serializers.ModelSerializer):
    """Serializer for ProfitLoss model"""
    profit_margin = serializers.SerializerMethodField()

    class Meta:
        model = ProfitLoss
        fields = [
            'id', 'period_start', 'period_end', 'total_revenue',
            'total_cost_of_goods_sold', 'total_expenses', 'gross_profit',
            'net_profit', 'profit_margin', 'created_at'
        ]
        read_only_fields = [
            'total_revenue', 'total_cost_of_goods_sold', 'total_expenses',
            'gross_profit', 'net_profit', 'created_at', 'profit_margin'
        ]

    def get_profit_margin(self, obj):
        """Calculate profit margin percentage"""
        if obj.total_revenue > 0:
            return float((obj.net_profit / obj.total_revenue) * 100)
        return 0.0

