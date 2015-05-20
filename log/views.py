from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import TechLogEntry

def logentry(request):
    return None

#  c.f. https://docs.djangoproject.com/en/1.8/topics/class-based-views/generic-display/
class LogEntryList(ListView):
    model = TechLogEntry
