# Generated by Django 3.2.8 on 2021-12-11 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_criteria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='favorites',
        ),
    ]
