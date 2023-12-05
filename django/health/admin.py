from django.contrib import admin
from django.db.models import ManyToManyField, ForeignKey
from django.utils import timezone
from . import models


def custom_permission(self, request):
    """
    If specific, custom permissions are needed (e.g. user can only change/delete their own object)
    then call this function via the following methods on a ModelAdmin below:
    - has_change_permission(self, request, obj=None)
    - has_delete_permission(self, request, obj=None)

    self = the ModelAdmin class (or inherited class), which calls this during a method
    request = the request in the ModelAdmin, which contains info about user, path, etc.
    """
    pass
    # path = request.path.split('/')  # e.g. '/dashboard/pages/page/1/change/'

    # # If an object is being changed or deleted, as specified in request path
    # if len(path) > 3 and path[-2] in ['change', 'delete']:

    #     # Ensure it only checks for the current model, as specified in request path
    #     if self.model._meta.model_name == path[3]:
    #         # Admins can change/delete all
    #         if request.user.role.name == 'admin':
    #             return True
    #         # Collaborators
    #         elif request.user.role.name == 'collaborator':
    #             try:
    #                 current_obj = self.model.objects.get(id=int(path[-3]))
    #                 # Can change/delete if it's their own (i.e. if they created it)
    #                 if current_obj.meta_created_by == request.user:
    #                     return True
    #                 # Can change (but not delete) if collaborator is marked as an editor
    #                 elif path[-2] == 'change' and hasattr(self.model, 'admin_editors') and request.user in current_obj.admin_editors.all():
    #                     return True
    #             except (AttributeError, ObjectDoesNotExist):
    #                 pass

    # # Deny access if no above condition has been met
    # return False


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
                     'cancer_champion_reflection',
                     'author__username')
    exclude = ('author',
               'created',
               'last_updated')

    def save_model(self, request, obj, form, change):
        # Automatically set author to current user
        if obj.author is None:
            obj.author = request.user

        # Automatically set last_updated to current datetime
        obj.last_updated = timezone.now()

        obj.save()
