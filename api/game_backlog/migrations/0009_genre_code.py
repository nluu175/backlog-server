# Generated by Django 5.0.4 on 2024-06-24 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_backlog', '0008_rename_title_game_name_remove_game_app_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='code',
            field=models.CharField(default='', max_length=100),
        ),
    ]
