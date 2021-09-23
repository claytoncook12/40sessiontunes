# Generated by Django 3.2.7 on 2021-09-23 15:45

from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):

    dependencies = [
        ('tunes', '0010_referenceaudio_repeats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referenceaudio',
            name='audio_file',
            field=models.FileField(upload_to=pathlib.PureWindowsPath('C:/Users/clayt/Documents/PythonFiles/40SessionTunes/DjangoApp/media/ReferenceAudio'), verbose_name='Reference Audio MP3 file'),
        ),
        migrations.AlterField(
            model_name='referenceaudio',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description of reference audio'),
        ),
    ]
