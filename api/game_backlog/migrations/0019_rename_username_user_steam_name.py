# Generated by Django 5.0.4 on 2024-08-26 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("game_backlog", "0018_backlog_favourite"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user", old_name="username", new_name="steam_name",
        ),
    ]
