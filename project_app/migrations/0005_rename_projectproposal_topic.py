# Generated by Django 3.2 on 2021-04-21 15:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_app', '0004_projectproposal_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProjectProposal',
            new_name='Topic',
        ),
    ]
