from django.db import migrations
from django.db import transaction
from django.conf import settings
from django.contrib.auth.hashers import make_password
from account import models
import csv
import os


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


def insert_participants(apps, schema_editor):
    """
    For each strand, read in the usernames and passwords of a list of participant users from a csv file
    Create new user accounts (ignore usernames that already exist in the database)
    """

    for participant_strand in ['health', 'education']:
        # Open the csv file for this participant_strand
        PARTICIPANTS_CSV = os.path.join(
            settings.BASE_DIR,
            'account',
            'participants',
            f'participants_{participant_strand}.csv'
        )
        # Get related data objects
        role = models.UserRole.objects.get(name='participant')
        participant_strand = models.ParticipantStrand.objects.get(name=participant_strand)
        try:
            with open(PARTICIPANTS_CSV, newline='') as csv_file:
                participants = csv.reader(csv_file)
                for participant in participants:
                    # Get data from record in csv
                    username = participant[0].replace('\ufeff', '')
                    password = make_password(participant[1])
                    # If user with this username doesn't already exist, create them
                    if not len(models.User.objects.filter(username=username)):
                        models.User.objects.create(
                            username=username,
                            role=role,
                            participant_strand=participant_strand,
                            password=password
                        )
        except FileNotFoundError as err:
            print(err)


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_user_roles),
        migrations.RunPython(insert_participant_strands),
        migrations.RunPython(insert_participants)
    ]
