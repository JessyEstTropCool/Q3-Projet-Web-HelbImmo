# Generated by Django 3.2.9 on 2021-12-16 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20211214_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='latitude',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='post',
            name='longitude',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=13),
        ),
    ]
