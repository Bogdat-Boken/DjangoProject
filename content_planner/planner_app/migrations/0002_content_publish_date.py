# Generated by Django 4.2.19 on 2025-02-23 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='publish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
