# Generated by Django 3.2.9 on 2021-11-25 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20211125_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='to_sell',
            field=models.BooleanField(default=True),
        ),
    ]