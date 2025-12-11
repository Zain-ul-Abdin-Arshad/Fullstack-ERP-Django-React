"""
URL configuration for Accounts API endpoints
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, LedgerEntryViewSet, ProfitLossViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'ledger', LedgerEntryViewSet, basename='ledgerentry')
router.register(r'profit-loss', ProfitLossViewSet, basename='profitloss')

urlpatterns = [
    path('', include(router.urls)),
]

