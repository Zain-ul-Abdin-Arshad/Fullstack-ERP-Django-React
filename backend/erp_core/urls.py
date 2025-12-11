
"""
URL configuration for erp_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

@require_http_methods(["GET"])
def api_root(request):
    """API root endpoint with available endpoints information"""
    return JsonResponse({
        'message': 'ERP System API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'authentication': {
                'login': '/api/token/',
                'refresh': '/api/token/refresh/',
            },
            'api': {
                'inventory': '/api/inventory/',
                'vendors': '/api/vendors/',
                'clients': '/api/clients/',
                'purchases': '/api/purchases/',
                'sales': '/api/sales/',
                'accounts': '/api/accounts/',
            }
        },
        'documentation': 'See API documentation for detailed endpoint information'
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('api/inventory/', include('inventory.urls')),
    path('api/vendors/', include('vendors.urls')),
    path('api/clients/', include('clients.urls')),
    path('api/purchases/', include('purchases.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/accounts/', include('accounts.urls')),
]
