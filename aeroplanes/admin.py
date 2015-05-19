from django.contrib import admin
from .models import Aeroplane

@admin.register(Aeroplane)
class AeroplaneAdmin(admin.ModelAdmin):
    pass
