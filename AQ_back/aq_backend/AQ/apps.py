from django.apps import AppConfig


class AqConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AQ'

    def ready(self):
        from AQ.firebase_sync import start_sync_thread
        start_sync_thread()