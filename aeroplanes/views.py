from django.shortcuts import render, get_object_or_404
from .models import Aeroplane
from .forms import AeroplaneForm

def aeroplane(request, aeroplane_id):
    ac = get_object_or_404(Aeroplane, pk=aeroplane_id)
    form = AeroplaneForm(instance=ac)
    return render(request, "aeroplanes/aeroplane.html", {"aeroplane": ac, "form": form})
