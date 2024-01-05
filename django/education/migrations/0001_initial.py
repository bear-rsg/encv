# Generated by Django 4.2.8 on 2024-01-05 12:39

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalEntryPrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, unique=True)),
                ('order', models.IntegerField(blank=True, null=True, unique=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('link_to_questionnaire', models.URLField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='questionnaire', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('limit_to_certain_participants', models.ManyToManyField(blank=True, help_text='If you wish to limit which participants see this questionnaire, double click their username above. If nobody is selected then all participants in the Education strand will see this questionnaire.', related_name='questionnaire_limit_to_certain_participants', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='Optional if providing content in another format below, e.g. audio/video', null=True)),
                ('link', models.URLField(blank=True, help_text="Optional. If you'd like to support your journal entry with a link to a web page, please provide the full URL here, e.g. https://www.example.com", null=True)),
                ('image', models.ImageField(blank=True, help_text="Optional. If you'd like to support your journal entry with an image, you can upload an image file", null=True, upload_to='education/journal_entry/image')),
                ('audio', models.FileField(blank=True, help_text="Optional. If you'd rather speak than type your journal entry, you can upload an audio file", null=True, upload_to='education/journal_entry/audio')),
                ('video', models.FileField(blank=True, help_text="Optional. If you'd rather create a visual journal entry, you can upload a video file", null=True, upload_to='education/journal_entry/video')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='journal_entries', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('prompt', models.ManyToManyField(blank=True, related_name='journal_entries', to='education.journalentryprompt')),
            ],
            options={
                'verbose_name_plural': 'journal entries',
                'ordering': ['-created'],
            },
        ),
    ]
