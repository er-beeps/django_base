from django.contrib import admin
from django.apps import apps
from .models import *
from django.contrib.admin.sites import AlreadyRegistered 

# Register your models here.

master_models = apps.get_app_config('master').get_models()
for model in master_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass

class DefaultAdmin(admin.ModelAdmin):
    pass

