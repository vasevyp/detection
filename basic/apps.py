from django.apps import AppConfig


class BasicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basic'
    verbose_name='Данные для анализа'
