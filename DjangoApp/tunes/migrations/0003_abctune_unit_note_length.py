# Generated by Django 3.2.7 on 2021-09-10 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tunes', '0002_unitnotelength'),
    ]

    operations = [
        migrations.AddField(
            model_name='abctune',
            name='unit_note_length',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tunes.unitnotelength', verbose_name='Unit Note Length'),
            preserve_default=False,
        ),
    ]
