from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "events"

from django.apps import AppConfig

class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'

    def ready(self):
        import events.signals  # 確保這一行沒有縮排錯誤
