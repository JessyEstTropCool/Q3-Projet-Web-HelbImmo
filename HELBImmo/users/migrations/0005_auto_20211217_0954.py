# Generated by Django 3.2.9 on 2021-12-17 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_profile_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='criteria',
            name='locality',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='criteria',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
