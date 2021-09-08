# Generated by Django 3.2.7 on 2021-09-08 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_type_char', models.CharField(max_length=15, unique=True, verbose_name='Key')),
            ],
        ),
        migrations.CreateModel(
            name='TuneType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tune_type_char', models.CharField(max_length=50, unique=True, verbose_name='Tune Type')),
            ],
        ),
        migrations.CreateModel(
            name='Tune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Tune Name')),
                ('tune_info', models.CharField(blank=True, max_length=300, verbose_name='Information about the tune')),
                ('tune_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tunes.tunetype', verbose_name='Tune Type')),
            ],
        ),
    ]
