"""
Django Admin configuration for Accounts models
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Payment, LedgerEntry, ProfitLoss


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'payment_type', 'get_party', 'amount', 
        'payment_method', 'reference_number', 'is_reconciled', 'created_at'
    ]
    list_filter = [
        'payment_type', 'payment_method', 'date', 'is_reconciled', 'created_at'
    ]
    search_fields = [
        'vendor__name', 'client__name', 'description', 
        'reference_number', 'amount'
    ]
    list_editable = ['is_reconciled']
    ordering = ['-date', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['vendor', 'client', 'purchase_order', 'sales_order']
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_type', 'amount', 'payment_method', 'date')
        }),
        ('Party Information', {
            'fields': ('vendor', 'client'),
            'description': 'Select either vendor OR client, not both'
        }),
        ('Related Orders', {
            'fields': ('purchase_order', 'sales_order')
        }),
        ('Details', {
            'fields': ('description', 'reference_number', 'is_reconciled')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_party(self, obj):
        """Display vendor or client name"""
        if obj.vendor:
            return f"Vendor: {obj.vendor.name}"
        elif obj.client:
            return f"Client: {obj.client.name}"
        return "-"
    get_party.short_description = 'Party'


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'entry_type', 'description_short', 
        'debit_amount', 'credit_amount', 'get_balance', 'created_at'
    ]
    list_filter = [
        'entry_type', 'date', 'created_at'
    ]
    search_fields = [
        'description', 'reference_type', 'reference_id'
    ]
    ordering = ['-date', '-created_at']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Entry Information', {
            'fields': ('date', 'entry_type', 'description')
        }),
        ('Amounts', {
            'fields': ('debit_amount', 'credit_amount')
        }),
        ('References', {
            'fields': ('payment', 'reference_type', 'reference_id')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def description_short(self, obj):
        """Display shortened description"""
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'

    def get_balance(self, obj):
        """Display balance for this entry"""
        balance = obj.credit_amount - obj.debit_amount
        color = 'green' if balance >= 0 else 'red'
        return format_html(
            '<span style="color: {};">${}</span>',
            color,
            balance
        )
    get_balance.short_description = 'Balance'


@admin.register(ProfitLoss)
class ProfitLossAdmin(admin.ModelAdmin):
    list_display = [
        'period_start', 'period_end', 'total_revenue', 
        'total_cost_of_goods_sold', 'gross_profit', 
        'total_expenses', 'net_profit', 'created_at'
    ]
    list_filter = ['period_start', 'period_end', 'created_at']
    search_fields = ['period_start', 'period_end']
    ordering = ['-period_end']
    readonly_fields = [
        'total_revenue', 'total_cost_of_goods_sold', 'total_expenses',
        'gross_profit', 'net_profit', 'created_at'
    ]
    fieldsets = (
        ('Period', {
            'fields': ('period_start', 'period_end')
        }),
        ('Revenue', {
            'fields': ('total_revenue',)
        }),
        ('Costs', {
            'fields': ('total_cost_of_goods_sold', 'total_expenses')
        }),
        ('Profit', {
            'fields': ('gross_profit', 'net_profit')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Disable manual addition - use calculate_profit_loss method"""
        return False

