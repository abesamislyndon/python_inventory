# Generated by Django 5.1.4 on 2025-01-20 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_client_event_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='theme_settings',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
