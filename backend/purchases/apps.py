"""
Django App configuration for Purchases module
"""

from django.apps import AppConfig


class PurchasesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchases'

    def ready(self):
        """Import signals when app is ready"""
        import purchases.signals

