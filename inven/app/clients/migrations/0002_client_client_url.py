# Generated by Django 5.1.4 on 2025-01-09 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='client_url',
            field=models.CharField(blank=True, null=True),
        ),
    ]
