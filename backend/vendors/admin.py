"""
Django Admin configuration for Vendor models
"""

from django.contrib import admin
from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'code', 'country', 'contact_number', 
        'email', 'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'country', 'created_at']
    search_fields = [
        'name', 'code', 'email', 'contact_number', 
        'country', 'city', 'tax_id'
    ]
    list_editable = ['is_active']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('email', 'contact_number', 'website')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Business Details', {
            'fields': ('tax_id', 'payment_terms', 'credit_limit')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

