from django.conf import settings
from django.contrib.auth.hashers import make_password
from account import models
import csv
import os


def add_participants(participant_strand):
    """
    Read in the usernames and passwords of a list of participant users from a csv file
    Create new user accounts (ignore usernames that already exist in the database)

    This script is intended to be run within the console in the django/ dir, using the command:
    python manage.py shell < account/add_participants.py
    """
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


# Call above function for both of the project strands
add_participants('education')
add_participants('health')
