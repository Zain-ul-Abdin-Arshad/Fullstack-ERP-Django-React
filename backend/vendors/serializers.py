"""
Django REST Framework Serializers for Vendors module
"""

from rest_framework import serializers
from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    """Serializer for Vendor model"""
    full_address = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = [
            'id', 'name', 'code', 'country', 'contact_number', 'email',
            'address', 'city', 'state', 'postal_code', 'website', 'tax_id',
            'payment_terms', 'credit_limit', 'is_active', 'notes',
            'full_address', 'items_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'items_count']

    def get_full_address(self, obj):
        """Get formatted full address"""
        return obj.get_full_address()

    def get_items_count(self, obj):
        """Get count of items from this vendor"""
        return obj.items.count()

