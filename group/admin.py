from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from .models import GroupProfile, GroupRole


@admin.register(GroupRole)
class GroupRoleAdmin(admin.ModelAdmin):
    pass

class GroupProfile(admin.StackedInline):
    model = GroupProfile
    can_delete = False
    verbose_name_plural = 'group profiles'

# Define a new User admin
class GroupAdmin(GroupAdmin):
    inlines = (GroupProfile, )


# Re-register UserAdmin
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

