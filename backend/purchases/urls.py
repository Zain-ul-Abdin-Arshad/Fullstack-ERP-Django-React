"""
URL configuration for Purchases API endpoints
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurchaseOrderViewSet, PurchaseItemViewSet

router = DefaultRouter()
router.register(r'orders', PurchaseOrderViewSet, basename='purchaseorder')
router.register(r'items', PurchaseItemViewSet, basename='purchaseitem')

urlpatterns = [
    path('', include(router.urls)),
]

