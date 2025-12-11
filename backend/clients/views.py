"""
Django REST Framework Viewsets for Clients module
"""

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet for Client model"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'country', 'city', 'client_type']
    search_fields = ['name', 'code', 'email', 'contact_number', 'country', 'city']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']

