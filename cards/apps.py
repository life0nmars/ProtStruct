"""
Конфигурация приложения
"""
from django.apps import AppConfig

class CardsConfig(AppConfig):
    """
    Класс для связи с приложением и его БД
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cards'
