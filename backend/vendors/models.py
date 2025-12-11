"""
Vendor/Supplier Management Models
Complete Vendor model for managing suppliers and vendors
"""

from django.db import models
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


class Vendor(models.Model):
    """
    Vendor/Supplier model for managing suppliers and vendors
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_("Vendor Name"),
        help_text=_("Name of the vendor/supplier company")
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("Vendor Code"),
        help_text=_("Short code for the vendor")
    )
    country = models.CharField(
        max_length=100,
        verbose_name=_("Country"),
        help_text=_("Country where the vendor is located")
    )
    contact_number = models.CharField(
        max_length=20,
        verbose_name=_("Contact Number"),
        help_text=_("Primary contact phone number")
    )
    email = models.EmailField(
        verbose_name=_("Email Address"),
        help_text=_("Primary email address"),
        validators=[EmailValidator()]
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Address"),
        help_text=_("Street address")
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("City")
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("State/Province")
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Postal Code")
    )
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Website"),
        help_text=_("Company website URL")
    )
    tax_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Tax ID"),
        help_text=_("Tax identification number")
    )
    payment_terms = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Payment Terms"),
        help_text=_("Standard payment terms (e.g., Net 30, Net 60)")
    )
    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Credit Limit"),
        help_text=_("Maximum credit limit for this vendor")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this vendor is currently active")
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Notes"),
        help_text=_("Additional notes about the vendor")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    class Meta:
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['code']),
            models.Index(fields=['country']),
            models.Index(fields=['is_active']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.name

    def get_full_address(self):
        """Return formatted full address"""
        parts = []
        if self.address:
            parts.append(self.address)
        if self.city:
            parts.append(self.city)
        if self.state:
            parts.append(self.state)
        if self.postal_code:
            parts.append(self.postal_code)
        if self.country:
            parts.append(self.country)
        return ", ".join(parts) if parts else ""

