from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from .models import GroupProfile, GroupContact, GroupMemberProfile


@admin.register(GroupContact)
class GroupRoleAdmin(admin.ModelAdmin):
    pass

class GroupProfile(admin.StackedInline):
    model = GroupProfile
    can_delete = False
    verbose_name_plural = 'group profiles'

@admin.register(GroupMemberProfile)
class GroupMemberProfileAdmin(admin.ModelAdmin):
    pass

# Define a new User admin
class GroupAdmin(GroupAdmin):
    inlines = (GroupProfile, )


# Re-register UserAdmin
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

