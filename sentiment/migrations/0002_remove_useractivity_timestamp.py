# Generated by Django 5.0.3 on 2024-03-13 10:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("sentiment", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="useractivity",
            name="timestamp",
        ),
    ]
