"""
Django REST Framework Viewsets for Vendors module
"""

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Vendor
from .serializers import VendorSerializer


class VendorViewSet(viewsets.ModelViewSet):
    """ViewSet for Vendor model"""
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'country', 'city']
    search_fields = ['name', 'code', 'email', 'contact_number', 'country', 'city']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']

