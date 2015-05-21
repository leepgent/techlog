from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView
from aeroplanes.models import Aeroplane
from .models import TechLogEntry

def logentry(request):
    return None

#  c.f. https://docs.djangoproject.com/en/1.8/topics/class-based-views/generic-display/
class LogEntryList(ListView):
    def get_queryset(self):
        self.aeroplane = get_object_or_404(Aeroplane, registration=self.kwargs["aeroplane_reg"])
        return TechLogEntry.objects.filter(aeroplane=self.aeroplane)
