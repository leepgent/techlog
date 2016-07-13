from django.contrib import admin
from . import models


@admin.register(models.TechLogEntry)
class TechLogAdmin(admin.ModelAdmin):
    list_filter = ['aeroplane__registration', 'commander']
    date_hierarchy = 'departure_time'
    ordering = ['-departure_time']


@admin.register(models.ConsumablesReceipt)
class ConsumablesReceiptAdmin(admin.ModelAdmin):
    list_filter = ['log_entry__aeroplane__registration', 'log_entry__commander']
    ordering = ['-log_entry__departure_time']

