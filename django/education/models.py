from django.db import models
from django.utils import timezone
from django.utils.text import Truncator
from django.utils.html import strip_tags
from ckeditor_uploader.fields import RichTextUploadingField
from account.models import User


class JournalEntry(models.Model):
    """
    An entry in a journal
    """

    related_name = 'journal_entries'
    upload_to_root = 'education/journal_entry/'

    text = RichTextUploadingField(
        blank=True,
        null=True,
        help_text="Optional if providing content in another format below, e.g. audio/video"
    )
    link = models.URLField(
        blank=True,
        null=True,
        help_text="Optional. If you'd like to support your journal entry with a link to a web page, please provide the full URL here, e.g. https://www.example.com"
    )
    image = models.ImageField(
        upload_to=f'{upload_to_root}image',
        blank=True,
        null=True,
        help_text="Optional. If you'd like to support your journal entry with an image, you can upload an image file "
    )
    audio = models.FileField(
        upload_to=f'{upload_to_root}audio',
        blank=True,
        null=True,
        help_text="Optional. If you'd rather speak than type your journal entry, you can upload an audio file"
    )
    video = models.FileField(
        upload_to=f'{upload_to_root}video',
        blank=True,
        null=True,
        help_text="Optional. If you'd rather create a visual journal entry, you can upload a video file"
    )

    author = models.ForeignKey(User, related_name=related_name, on_delete=models.PROTECT, blank=True, null=True, verbose_name="created by")
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(blank=True, null=True)

    @property
    def name(self):
        return f'Journal Entry: {self.author.username} ({self.created.date()} {str(self.created.time())[:5]})'

    @property
    def text_preview(self):
        return strip_tags(Truncator(self.text).chars(100))

    @property
    def view_journal_entry(self):
        return 'View'

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'journal entries'


class Questionnaire(models.Model):
    """
    A link to a questionnaire offered by an external provider
    """

    related_name = 'questionnaire'

    title = models.CharField(max_length=255)
    link_to_questionnaire = models.URLField()

    author = models.ForeignKey(User, related_name=related_name, on_delete=models.PROTECT, blank=True, null=True, verbose_name="created by")
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(blank=True, null=True)

    @property
    def view_questionnaire(self):
        return 'View'

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
