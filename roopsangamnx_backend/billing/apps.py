from django.apps import AppConfig


class BillingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'billing'
    def ready(self):
        from billing import printer
        printer.initialize_printer()
