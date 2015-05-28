from django.contrib import admin
from .models import TechLogEntry, Check


@admin.register(TechLogEntry)
class TechLogAdmin(admin.ModelAdmin):
    pass

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    pass
