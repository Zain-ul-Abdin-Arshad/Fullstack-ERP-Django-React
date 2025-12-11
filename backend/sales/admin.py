"""
Django Admin configuration for Sales models
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import SalesOrder, SalesItem


class SalesItemInline(admin.TabularInline):
    """Inline admin for sales items"""
    model = SalesItem
    extra = 1
    fields = [
        'item', 'quantity', 'unit_price', 'discount_percentage', 
        'line_total', 'shipped_quantity'
    ]
    readonly_fields = ['line_total']
    autocomplete_fields = ['item']


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'client', 'order_date', 'status', 
        'total_amount', 'get_item_count', 'warehouse', 'created_at'
    ]
    list_filter = [
        'status', 'order_date', 'client', 'warehouse', 'created_at'
    ]
    search_fields = [
        'order_number', 'client__name', 'client__code', 'notes'
    ]
    list_editable = ['status']
    ordering = ['-order_date', '-created_at']
    readonly_fields = [
        'total_amount', 'created_at', 'updated_at', 
        'shipped_date', 'delivered_date'
    ]
    autocomplete_fields = ['client', 'warehouse']
    inlines = [SalesItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'client', 'order_date', 'status', 'warehouse')
        }),
        ('Delivery', {
            'fields': ('expected_delivery_date', 'shipped_date', 'delivered_date')
        }),
        ('Financial', {
            'fields': ('total_amount', 'discount_amount')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_shipped', 'mark_as_delivered', 'cancel_orders']

    def get_item_count(self, obj):
        """Display item count"""
        return obj.get_item_count()
    get_item_count.short_description = 'Items'

    def mark_as_shipped(self, request, queryset):
        """Admin action to mark orders as shipped"""
        count = 0
        for order in queryset:
            if order.status not in ['SHIPPED', 'DELIVERED']:
                order.mark_as_shipped()
                count += 1
        self.message_user(request, f'{count} order(s) marked as shipped.')
    mark_as_shipped.short_description = 'Mark selected orders as shipped'

    def mark_as_delivered(self, request, queryset):
        """Admin action to mark orders as delivered"""
        count = 0
        for order in queryset:
            if order.status != 'DELIVERED':
                order.mark_as_delivered()
                count += 1
        self.message_user(request, f'{count} order(s) marked as delivered.')
    mark_as_delivered.short_description = 'Mark selected orders as delivered'

    def cancel_orders(self, request, queryset):
        """Admin action to cancel orders"""
        count = 0
        for order in queryset:
            if order.status != 'CANCELLED':
                order.cancel_order()
                count += 1
        self.message_user(request, f'{count} order(s) cancelled.')
    cancel_orders.short_description = 'Cancel selected orders'


@admin.register(SalesItem)
class SalesItemAdmin(admin.ModelAdmin):
    list_display = [
        'sales_order', 'item', 'quantity', 'unit_price', 
        'discount_percentage', 'line_total', 'shipped_quantity'
    ]
    list_filter = [
        'sales_order__status', 'sales_order__order_date', 'created_at'
    ]
    search_fields = [
        'sales_order__order_number', 'item__name', 'item__sku'
    ]
    readonly_fields = [
        'line_total', 'created_at', 'updated_at'
    ]
    autocomplete_fields = ['sales_order', 'item']
    ordering = ['sales_order', 'item']
    fieldsets = (
        ('Order Information', {
            'fields': ('sales_order', 'item')
        }),
        ('Quantity', {
            'fields': ('quantity', 'shipped_quantity')
        }),
        ('Pricing', {
            'fields': ('unit_price', 'discount_percentage', 'line_total')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

