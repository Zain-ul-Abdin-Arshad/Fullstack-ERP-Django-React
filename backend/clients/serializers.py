"""
Django REST Framework Serializers for Clients module
"""

from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model"""
    full_address = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    sales_orders_count = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'id', 'name', 'code', 'country', 'city', 'contact_number', 'email',
            'address', 'state', 'postal_code', 'website', 'tax_id',
            'payment_terms', 'credit_limit', 'discount_percentage',
            'is_active', 'client_type', 'notes', 'full_address', 'location',
            'sales_orders_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'sales_orders_count']

    def get_full_address(self, obj):
        """Get formatted full address"""
        return obj.get_full_address()

    def get_location(self, obj):
        """Get city and country"""
        return obj.get_location()

    def get_sales_orders_count(self, obj):
        """Get count of sales orders"""
        return obj.sales_orders.count()

