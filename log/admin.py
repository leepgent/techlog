from django.contrib import admin
from .models import TechLogEntry

@admin.register(TechLogEntry)
class TechLogAdmin(admin.ModelAdmin):
    pass
