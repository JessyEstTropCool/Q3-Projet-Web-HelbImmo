# Generated by Django 3.2.8 on 2021-12-11 18:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_postfavorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfavorite',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
