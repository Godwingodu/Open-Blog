# Generated by Django 4.1.7 on 2023-04-04 10:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0007_alter_follow_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='follow',
            new_name='follows',
        ),
    ]
