# Generated by Django 3.2.12 on 2023-04-05 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_follows_followers_alter_follows_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
