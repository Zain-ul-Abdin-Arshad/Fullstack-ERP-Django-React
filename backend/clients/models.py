"""
Client/Customer Management Models
Complete Client model for managing customers and clients
"""

from django.db import models
from django.core.validators import EmailValidator, MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    """
    Client/Customer model for managing customers and clients
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_("Client Name"),
        help_text=_("Name of the client/customer company or individual")
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("Client Code"),
        help_text=_("Short code for the client")
    )
    country = models.CharField(
        max_length=100,
        verbose_name=_("Country"),
        help_text=_("Country where the client is located")
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_("City"),
        help_text=_("City where the client is located")
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
        help_text=_("Standard payment terms (e.g., Net 30, Net 60, COD)")
    )
    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Credit Limit"),
        help_text=_("Maximum credit limit for this client")
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Discount Percentage"),
        help_text=_("Standard discount percentage for this client")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this client is currently active")
    )
    client_type = models.CharField(
        max_length=20,
        choices=[
            ('INDIVIDUAL', 'Individual'),
            ('RETAILER', 'Retailer'),
            ('WHOLESALER', 'Wholesaler'),
            ('DISTRIBUTOR', 'Distributor'),
            ('DEALER', 'Dealer'),
            ('OTHER', 'Other'),
        ],
        default='RETAILER',
        verbose_name=_("Client Type"),
        help_text=_("Type of client/customer")
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Notes"),
        help_text=_("Additional notes about the client")
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
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['code']),
            models.Index(fields=['country']),
            models.Index(fields=['city']),
            models.Index(fields=['is_active']),
            models.Index(fields=['email']),
            models.Index(fields=['client_type']),
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

    def get_location(self):
        """Return city and country"""
        location_parts = []
        if self.city:
            location_parts.append(self.city)
        if self.country:
            location_parts.append(self.country)
        return ", ".join(location_parts) if location_parts else ""

