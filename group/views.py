from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from .models import GroupProfile, GroupMemberProfile


@login_required
def group(request, pk):
    groupprofile = get_object_or_404(GroupProfile, id=pk)
    return render(request, "group/group_detail.html", {"profile": groupprofile})


@login_required
def join_group(request, secret):
    user = request.user
    groupprofile = get_object_or_404(GroupProfile, secret_key=secret)
    group = groupprofile.group

    member_profile_exists = GroupMemberProfile.objects.filter(group=groupprofile, member=user).exists()

    if 'confirm' in request.GET:
        # Dead easy. Add our request user to the group and quit.
        # ...if they're not in there already!
        if member_profile_exists:
            return HttpResponseBadRequest("You are already a member of this Group!")

        group.user_set.add(user)

        group_member_profile = GroupMemberProfile()
        group_member_profile.group = groupprofile
        group_member_profile.member = user
        group_member_profile.administrator = False
        group_member_profile.current_rate_includes_fuel = groupprofile.default_rate_includes_fuel
        group_member_profile.current_rate_includes_oil = groupprofile.default_rate_includes_oil
        group_member_profile.current_charge_regime = groupprofile.default_charge_regime
        group_member_profile.current_cost_per_unit = groupprofile.default_cost_per_unit

        group_member_profile.save()

        return HttpResponseRedirect(reverse('dashboard'))

    if member_profile_exists:
        template = "group/group_already_joined.html"
    else:
        template = "group/group_join.html"

    return render(request, template, {"profile": groupprofile})


def creategroup(request):
    return render(request, "group/group_create.html")
