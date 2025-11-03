from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    settings_module = 'main.settings'
    urls_module = 'main.urls'