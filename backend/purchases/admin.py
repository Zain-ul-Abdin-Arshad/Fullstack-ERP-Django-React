"""
Django Admin configuration for Purchase models
"""

from django.contrib import admin
from .models import PurchaseOrder, PurchaseItem


class PurchaseItemInline(admin.TabularInline):
    """Inline admin for purchase items"""
    model = PurchaseItem
    extra = 1
    fields = [
        'item', 'quantity', 'unit_cost', 'freight_cost', 
        'customs_duty', 'other_costs', 'line_total', 
        'landed_cost_per_unit', 'total_landed_cost', 'received_quantity'
    ]
    readonly_fields = ['line_total', 'landed_cost_per_unit', 'total_landed_cost']
    autocomplete_fields = ['item']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'vendor', 'order_date', 'status', 
        'total_amount', 'get_item_count', 'created_at'
    ]
    list_filter = ['status', 'order_date', 'vendor', 'created_at']
    search_fields = [
        'order_number', 'vendor__name', 'vendor__code', 'notes'
    ]
    list_editable = ['status']
    ordering = ['-order_date', '-created_at']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    autocomplete_fields = ['vendor']
    inlines = [PurchaseItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'vendor', 'order_date', 'status')
        }),
        ('Delivery', {
            'fields': ('expected_delivery_date', 'received_date')
        }),
        ('Financial', {
            'fields': ('total_amount',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_item_count(self, obj):
        """Display item count"""
        return obj.get_item_count()
    get_item_count.short_description = 'Items'


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = [
        'purchase_order', 'item', 'quantity', 'unit_cost', 
        'landed_cost_per_unit', 'total_landed_cost', 'received_quantity'
    ]
    list_filter = ['purchase_order__status', 'purchase_order__order_date', 'created_at']
    search_fields = [
        'purchase_order__order_number', 'item__name', 'item__sku'
    ]
    readonly_fields = [
        'line_total', 'landed_cost_per_unit', 'total_landed_cost', 
        'created_at', 'updated_at'
    ]
    autocomplete_fields = ['purchase_order', 'item']
    ordering = ['purchase_order', 'item']
    fieldsets = (
        ('Order Information', {
            'fields': ('purchase_order', 'item')
        }),
        ('Quantity', {
            'fields': ('quantity', 'received_quantity')
        }),
        ('Costs', {
            'fields': ('unit_cost', 'freight_cost', 'customs_duty', 'other_costs')
        }),
        ('Calculated Values', {
            'fields': (
                'line_total', 'landed_cost_per_unit', 'total_landed_cost'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

