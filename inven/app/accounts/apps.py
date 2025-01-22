from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.accounts'  # Replace this with your actual app name

    def ready(self):
        import app.accounts.signals  # Import the signals file
