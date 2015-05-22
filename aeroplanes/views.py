from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Aeroplane
from .forms import AeroplaneForm

@login_required
def aeroplane(request, aeroplane_reg):
    ac = get_object_or_404(Aeroplane, registration=aeroplane_reg)
    form = AeroplaneForm(instance=ac)
    return render(request, "aeroplanes/aeroplane.html", {"aeroplane": ac, "form": form})
