# Generated by Django 4.2.16 on 2024-11-23 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadhistory',
            name='detected_plate_numbers',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadhistory',
            name='detected_states',
            field=models.TextField(blank=True, null=True),
        ),
    ]
