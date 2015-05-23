from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import GroupProfile

@login_required
def group(request, pk):
    groupprofile = get_object_or_404(GroupProfile, id=pk)
    return render(request, "group/group_detail.html", {"profile": groupprofile})



@login_required
def joingroup(request, secret):
    groupprofile = get_object_or_404(GroupProfile, secret_key=secret)

    if 'confirm' in request.GET:
        # Dead easy. Add our request user to the group and quit.
        group = groupprofile.group
        group.user_set.add(request.user)
        return HttpResponseRedirect(reverse('dashboard'))

    return render(request, "group/group_join.html", {"profile": groupprofile})
