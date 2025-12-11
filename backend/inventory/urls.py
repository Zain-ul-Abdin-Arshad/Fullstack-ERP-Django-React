"""
URL configuration for Inventory API endpoints
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, WarehouseViewSet, ItemViewSet, StockViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'items', ItemViewSet, basename='item')
router.register(r'stock', StockViewSet, basename='stock')

urlpatterns = [
    path('', include(router.urls)),
]

