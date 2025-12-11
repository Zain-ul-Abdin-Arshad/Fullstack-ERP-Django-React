"""
Django Admin configuration for Inventory models
"""

from django.contrib import admin
from .models import Category, Warehouse, Item, Stock, StockAlert


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'parent']
    search_fields = ['name', 'code', 'description']
    list_editable = ['is_active']
    ordering = ['name']
    prepopulated_fields = {'code': ('name',)}


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'city', 'country', 'is_active', 'created_at']
    list_filter = ['is_active', 'country', 'created_at']
    search_fields = ['name', 'code', 'address', 'city', 'manager_name']
    list_editable = ['is_active']
    ordering = ['name']
    prepopulated_fields = {'code': ('name',)}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'sku', 'category', 'vendor', 'cost_price', 
        'selling_price', 'unit', 'is_active', 'created_at'
    ]
    list_filter = [
        'category', 'vendor', 'is_active', 'is_trackable', 
        'unit', 'created_at'
    ]
    search_fields = [
        'name', 'sku', 'barcode', 'description', 
        'vehicle_make', 'vehicle_model'
    ]
    list_editable = ['is_active', 'cost_price', 'selling_price']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'sku', 'barcode', 'description', 'category', 'vendor')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price')
        }),
        ('Inventory', {
            'fields': ('unit', 'reorder_level', 'reorder_quantity', 'is_trackable', 'allow_backorder')
        }),
        ('Physical Attributes', {
            'fields': ('weight', 'dimensions')
        }),
        ('Vehicle Compatibility', {
            'fields': ('vehicle_make', 'vehicle_model', 'vehicle_year_from', 'vehicle_year_to')
        }),
        ('Status', {
            'fields': ('is_active', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = [
        'item', 'warehouse', 'quantity', 'reserved_quantity', 
        'available_quantity', 'min_quantity', 'is_low_stock', 'updated_at'
    ]
    list_filter = ['warehouse', 'created_at', 'updated_at']
    search_fields = ['item__name', 'item__sku', 'warehouse__name']
    list_editable = ['quantity', 'reserved_quantity', 'min_quantity']
    ordering = ['item', 'warehouse']
    readonly_fields = ['available_quantity', 'created_at', 'updated_at']
    autocomplete_fields = ['item', 'warehouse']


@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    list_display = [
        'item', 'warehouse', 'current_quantity', 'min_quantity',
        'alert_status', 'created_at', 'acknowledged_at'
    ]
    list_filter = ['alert_status', 'warehouse', 'created_at']
    search_fields = ['item__name', 'item__sku', 'warehouse__name', 'message']
    list_editable = ['alert_status']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'acknowledged_at', 'resolved_at']
    actions = ['acknowledge_alerts', 'resolve_alerts']

    def acknowledge_alerts(self, request, queryset):
        """Admin action to acknowledge selected alerts"""
        count = 0
        for alert in queryset.filter(alert_status='PENDING'):
            alert.acknowledge()
            count += 1
        self.message_user(request, f'{count} alert(s) acknowledged.')
    acknowledge_alerts.short_description = 'Acknowledge selected alerts'

    def resolve_alerts(self, request, queryset):
        """Admin action to resolve selected alerts"""
        count = 0
        for alert in queryset.filter(alert_status__in=['PENDING', 'ACKNOWLEDGED']):
            alert.resolve()
            count += 1
        self.message_user(request, f'{count} alert(s) resolved.')
    resolve_alerts.short_description = 'Resolve selected alerts'

