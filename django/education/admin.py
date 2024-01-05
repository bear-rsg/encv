from django.contrib import admin
from django.db.models import ManyToManyField, ForeignKey
from django.utils.safestring import mark_safe
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


@admin.register(models.JournalEntryPrompt)
class JournalEntryPromptAdminView(GenericAdminView):
    """
    Customise the admin interface for JournalEntryPrompt model
    """

    search_fields = ('order', 'text',)
    list_display = ('order', 'text',)
    list_display_links = ('order', 'text',)

    def has_module_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'admin_only')

    def has_view_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'all_users_in_strand')

    def has_add_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'admin_only')

    def has_change_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'admin_only')

    def has_delete_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'admin_only')


@admin.register(models.JournalEntry)
class JournalEntryAdminView(GenericAdminView):
    """
    Customise the admin interface for JournalEntry model
    """

    list_display = ('view_journal_entry',
                    'text_preview',
                    'link',
                    'image',
                    'audio',
                    'video',
                    'author',
                    'created',
                    'last_updated')
    list_display_links = ('view_journal_entry',)
    list_filter = ('prompt',)
    search_fields = ('id',
                     'text',
                     'link',
                     'image',
                     'audio',
                     'video',
                     'author__username')
    exclude = ('author',
               'created',
               'last_updated')

    def has_module_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'all_users_in_strand')

    def has_view_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'all_users_in_strand')

    def has_add_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'all_users_in_strand')

    def has_change_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'all_users_in_strand_recently_created')

    def has_delete_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'admin_only')

    def get_queryset(self, request, obj=None):
        return custom_permissions.get_queryset_by_permission(self, request, 'hide_if_participant_is_not_author')

    def get_readonly_fields(self, request, obj=None):
        # Only show time_left_to_edit if the object is being edited (i.e. if object already exists)
        return ('time_left_to_edit',) if obj else []

    def save_model(self, request, obj, form, change):
        # Automatically set author to current user
        if obj.author is None:
            obj.author = request.user
        # Automatically set last_updated to current datetime
        obj.last_updated = timezone.now()
        # Save changes to object
        obj.save()


@admin.register(models.Questionnaire)
class QuestionnaireAdminView(GenericAdminView):
    """
    Customise the admin interface for Questionnaire model
    """

    search_fields = ('title',
                     'link_to_questionnaire',
                     'author__username')

    def changelist_view(self, request, extra_context=None):
        """
        Add the current user to the view to be used in other methods below
        """
        setattr(self, 'user', request.user)
        return super().changelist_view(request, extra_context)

    def get_list_display(self, request, obj=None):
        if request.user.role.name == 'participant':
            return ('title',
                    'link_to_complete_questionnaire',)
        else:
            return ('view_questionnaire',
                    'title',
                    'link_to_complete_questionnaire',
                    'author',
                    'created',
                    'last_updated')

    def get_list_display_links(self, request, obj=None):
        if request.user.role.name == 'participant':
            return None
        else:
            return ('view_questionnaire',)

    def get_exclude(self, request, obj=None):
        exclude = ['author', 'created', 'last_updated']
        if request.user.role.name == 'participant':
            exclude.append('link_to_questionnaire')
        return exclude

    def link_to_complete_questionnaire(self, obj=None):
        """
        Modify the questionnaire link to include the current participant's information
        """
        url = f'{obj.link_to_questionnaire}?username={self.user.username}&user_id={self.user.id}'
        return mark_safe(f'<a href="{url}" target="_blank">{url}</a>')

    def has_module_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'all_users_in_strand')

    def has_view_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'all_users_in_strand')

    def has_add_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'admin_only')

    def has_change_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'admin_only')

    def has_delete_permission(self, request, obj=None):
        return custom_permissions.get_permission(self, request, obj, 'admin_only')

    def get_queryset(self, request, obj=None):
        return custom_permissions.get_queryset_by_permission(self, request, 'limit_to_certain_participants')

    def save_model(self, request, obj, form, change):
        # Automatically set author to current user
        if obj.author is None:
            obj.author = request.user

        # Automatically set last_updated to current datetime
        obj.last_updated = timezone.now()

        obj.save()
