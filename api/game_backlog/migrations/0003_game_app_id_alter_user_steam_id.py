# Generated by Django 5.0.4 on 2024-05-26 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_backlog', '0002_backlog_comment_alter_backlog_id_alter_game_genres_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='app_id',
            field=models.CharField(default=None, max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='steam_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
