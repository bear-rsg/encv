from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


admin.site.site_header = 'ENCV: Empathy, Narrative and Cultural Values'
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Customise the admin interface: User
    """

    form = UserChangeForm
    model = User
    list_display = ['username', 'email', 'role', 'participant_strand', 'is_active', 'date_joined', 'last_login']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['role', 'participant_strand', 'is_active']
    readonly_fields = ['date_joined', 'last_login']
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role', 'is_active', 'date_joined', 'last_login')}),
        ('Participant', {'fields': ('participant_strand',)}),
        ('Admin', {'fields': ('email', 'first_name', 'last_name',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', 'role')}),
        ('Participant', {'fields': ('participant_strand',)}),
        ('Admin', {'fields': ('email', 'first_name', 'last_name',)})
    )

    def has_module_permission(self, request, obj=None):
        return not request.user.is_anonymous and request.user.is_admin

    def has_view_permission(self, request, obj=None):
        return not request.user.is_anonymous and request.user.is_admin

    def has_add_permission(self, request, obj=None):
        return not request.user.is_anonymous and request.user.is_admin

    def has_change_permission(self, request, obj=None):
        return not request.user.is_anonymous and request.user.is_admin

    def has_delete_permission(self, request, obj=None):
        # nobody can delete users via dashboard, must mark them as 'inactive' instead
        return False
