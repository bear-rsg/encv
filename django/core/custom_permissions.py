"""
Set custom permissions that need more control than using standard Django Groups and Permissions

Functions in this script are used in admin.py in different apps,
which is why they're stored in 'core' so can be shared between apps.
"""


from datetime import date, timedelta
from django.db.models import Q 


def get_permission(self, request, obj, permission):
    """
    Permit (return True) or deny (return False) access to the current action that calls this method.
    Used within has_view_permission(), has_view_permission(), etc. in a ModelAdmin.
    Pass one of the permission names mentioned below (e.g. 'admin_only') to apply that permission.
    """

    # Ensure user is logged in
    if request.user.is_authenticated:

        # Permit admins only
        if permission == 'admin_only':
            if request.user.role.name == 'admin':
                return True
        # Permit all users in this strand
        elif permission == 'all_users_in_strand':
            if request.user.role.name == 'admin' or request.user.participant_strand.name == self.model._meta.app_label:
                return True
        # Permit all users in this strand if object was created within the past 2 weeks
        elif permission == 'all_users_in_strand_recently_created':
            if (request.user.role.name == 'admin' or request.user.participant_strand.name == self.model._meta.app_label) and (obj and date.today() < (obj.created.date() + timedelta(days=14))):
                return True

    # Deny if none of above conditions found
    return False


def get_queryset_by_permission(self, request, queryset_permission):
    """
    Filter/exclude the current model's objects based on the specified queryset_permission.
    Used within get_queryset() in a ModelAdmin.
    Pass one of the queryset_permission names mentioned below (e.g. 'hide_if_participant_is_not_author')
    to apply that particular filter/exclude.
    """

    objects = self.model.objects.all()

    # Ensure user is logged in
    if request.user.is_authenticated:

        # Show objects if user is participant and the author of the object or if user is an admin
        if queryset_permission == 'hide_if_participant_is_not_author':
            if request.user.role.name == 'participant' and request.user.participant_strand.name == self.model._meta.app_label:
                return objects.filter(author=request.user)
            elif request.user.role.name == 'admin':
                return objects
        # Permit admins and only certain participants (if the limit_to_certain_participants field on object is set, otherwise allow all participants in strand)
        elif queryset_permission == 'limit_to_certain_participants':
            if request.user.role.name == 'participant' and request.user.participant_strand.name == self.model._meta.app_label:
                return objects.filter(
                    Q(limit_to_certain_participants__in=[request.user]) | Q(limit_to_certain_participants=None)
                )
            elif request.user.role.name == 'admin':
                return objects

    # Return empty queryset if none of above conditions found
    return None
