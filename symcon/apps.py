# -*- coding: UTF-8 -*-
from django.apps import AppConfig


class SymconConfig(AppConfig):
    name = 'symcon'

    def ready(self):
        import symcon.signals  #noqa
