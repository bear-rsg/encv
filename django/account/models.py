from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.functions import Upper
from django.db import models
import logging

logger = logging.getLogger(__name__)


class UserRole(models.Model):
    """
    Role for each user, e.g. Admin, Participant
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ParticipantStrand(models.Model):
    """
    The project strand that a participant can belong to, e.g. Health or Education
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        """
        Allow users to login with case-insensitive username

        E.g. both "My.Name@uni.ac.uk" and "my.name@uni.ac.uk" will allow users to login
        """
        return self.get(username__iexact=username)


class User(AbstractUser):
    """
    Custom user extends the standard Django user model, providing additional properties
    """

    # Custom user manager used to allow for case-insensitive usernames
    objects = CustomUserManager()

    # Add new fields on top of those provided in AbstractUser
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, blank=True, null=True)
    participant_strand = models.ForeignKey(ParticipantStrand, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def is_admin(self):
        return self.role and self.role.name == 'admin'

    @property
    def is_participant(self):
        return self.role and self.role.name == 'participant'

    @property
    def is_participant_education(self):
        return self.is_participant and self.participant_strand.name == 'education'

    @property
    def is_participant_health(self):
        return self.is_participant and self.participant_strand.name == 'health'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # All users are marked as staff so that they can all login to dashboard
        self.is_staff = True
        super().save(*args, **kwargs)

    class Meta:
        ordering = [Upper('username'), 'id']
