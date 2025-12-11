"""
URL configuration for Sales API endpoints
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesOrderViewSet, SalesItemViewSet

router = DefaultRouter()
router.register(r'orders', SalesOrderViewSet, basename='salesorder')
router.register(r'items', SalesItemViewSet, basename='salesitem')

urlpatterns = [
    path('', include(router.urls)),
]

