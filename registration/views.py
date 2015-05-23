from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from registration.forms import NewUserForm


def join(request):
    next = ""
    if request.method == "GET":
        form = NewUserForm()
        if 'next' in request.GET:
            next = request.GET['next']

    elif request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = authenticate(username=new_user.username, password=form.cleaned_data.get("password2"))
            login(request, user)
            if "next" in request.POST:
                next = request.POST["next"]
                if next:
                    return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse("dashboard"))

    return render(request, "registration/user_create.html", {"form": form, "next": next})
