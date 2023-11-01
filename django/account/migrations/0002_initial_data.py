from django.db import migrations
from django.db import transaction
from account import models
import sys


def insert_user_roles(apps, schema_editor):
    """
    Inserts UserRole objects
    """

    roles = ['admin', 'participant']

    for role in roles:
        with transaction.atomic():
            models.UserRole(name=role).save()


def insert_participant_strands(apps, schema_editor):
    """
    Inserts ParticipantStrand objects
    """

    participant_strands = ['education', 'health']

    for participant_strand in participant_strands:
        with transaction.atomic():
            models.ParticipantStrand(name=participant_strand).save()


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_user_roles),
        migrations.RunPython(insert_participant_strands),
    ]
