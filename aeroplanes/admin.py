from django.contrib import admin
from .models import Aeroplane, Check

@admin.register(Aeroplane)
class AeroplaneAdmin(admin.ModelAdmin):
    pass

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    pass