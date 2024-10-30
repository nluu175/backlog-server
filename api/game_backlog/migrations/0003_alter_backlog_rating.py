# Generated by Django 5.1.2 on 2024-10-24 07:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_backlog', '0002_backlog_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backlog',
            name='rating',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1, message='Rating must be at least 1'), django.core.validators.MaxValueValidator(5, message='Rating cannot exceed 5')]),
        ),
    ]