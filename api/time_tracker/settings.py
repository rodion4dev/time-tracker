"""Настройки проекта."""
import os

# Режим отладки приложения
DEBUG = os.environ.get('DEBUG', default='false').lower() == 'true'
