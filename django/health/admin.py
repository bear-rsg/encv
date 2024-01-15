from django.contrib import admin
from django.db.models import ManyToManyField, ForeignKey
from django.utils import timezone
from core import custom_permissions
from . import models


def get_manytomany_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of many to many fields of a model
    To ignore certain fields, provide a list of such fields using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) is ManyToManyField and f.name not in exclude)


def get_foreignkey_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of foreign key fields of a model
    To ignore certain fields, provide a list of such field names (as strings) using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) is ForeignKey and f.name not in exclude)


class GenericAdminView(admin.ModelAdmin):
    """
    This is a generic class that can be applied to most models to customise their inclusion in the Django admin.
    """

    list_per_page = 100

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all many to many fields to display the filter_horizontal widget
        self.filter_horizontal = get_manytomany_fields(self.model)
        # Set all foreign key fields to display the autocomplete widget
        self.autocomplete_fields = get_foreignkey_fields(self.model)


@admin.register(models.Conversation)
class ConversationAdminView(GenericAdminView):
    """
    Customise the admin interface for Conversation model
    """

    list_display = ('view_conversation',
                    'conversation_date',
                    'conversation_audio',
                    'cancer_champion_reflection_preview',
                    'author',
                    'created',
                    'last_updated')
    list_display_links = ('view_conversation',)
    search_fields = ('id',
                     'conversation_audio',
                     'cancer_champion_reflection',
                     'author__username')
    exclude = ('author',
               'created',
               'last_updated')

    def get_fields(self, request, obj=None):
        fields = [
            'conversation_date',
            'conversation_audio',
        ]
        if request.user.role.name == 'admin':
            fields += ['conversation_transcript',]
        fields += ['cancer_champion_reflection',]
        return fields

    def has_module_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'all_users_in_strand')

    def has_view_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'all_users_in_strand')

    def has_add_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'all_users_in_strand')

    def has_change_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'all_users_in_strand')

    def has_delete_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'admin_only')

    def get_queryset(self, request, obj=None):
        return custom_permissions.get_queryset_by_permission(self, request, 'hide_if_participant_is_not_author')

    def save_model(self, request, obj, form, change):
        # Automatically set author to current user
        if obj.author is None:
            obj.author = request.user

        # Automatically set last_updated to current datetime
        obj.last_updated = timezone.now()

        obj.save()
