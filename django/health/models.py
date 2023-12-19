from django.db import models
from django.utils import timezone
from django.utils.text import Truncator
from account.models import User


class Conversation(models.Model):
    """
    A conversation between a "cancer champion" and a cancer patient
    """

    related_name = 'conversations'

    conversation_date = models.DateField(help_text='Please input the date the conversation was held')
    conversation_audio = models.FileField(upload_to='health/conversation/audio', help_text='Please upload an audio recording of the conversation')
    conversation_transcript = models.FileField(
        blank=True,
        null=True,
        upload_to='health/conversation/transcript',
        help_text='Please upload a file containing the transcript of the conversation, e.g. a Word document.')
    cancer_champion_reflection = models.TextField(
        blank=True,
        null=True,
        help_text="Optional. If you're the 'cancer champion' please add any reflections or thoughts you have about this conversation."
    )

    author = models.ForeignKey(User, related_name=related_name, on_delete=models.PROTECT, blank=True, null=True, verbose_name='created by')
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(blank=True, null=True)

    @property
    def name(self):
        return f'Conversation: {self.author.username} ({self.conversation_date})'

    @property
    def cancer_champion_reflection_preview(self):
        return Truncator(self.cancer_champion_reflection).chars(100)

    @property
    def view_conversation(self):
        return 'View'

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']


class Video(models.Model):
    """
    A video upload for the health strand of the project
    """

    related_name = 'videos'

    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='health/video')
    description = models.TextField(blank=True, null=True)

    author = models.ForeignKey(User, related_name=related_name, on_delete=models.PROTECT, blank=True, null=True, verbose_name='created by')
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(blank=True, null=True)

    @property
    def view_video(self):
        return 'View'

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
