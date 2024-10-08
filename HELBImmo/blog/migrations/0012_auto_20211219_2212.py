# Generated by Django 3.2.8 on 2021-12-19 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20211216_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='country_code',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='post',
            name='latitude',
            field=models.DecimalField(decimal_places=10, max_digits=12),
        ),
        migrations.AlterField(
            model_name='post',
            name='longitude',
            field=models.DecimalField(decimal_places=10, max_digits=13),
        ),
        migrations.AlterField(
            model_name='post',
            name='region_city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='road_num',
            field=models.CharField(max_length=100),
        ),
    ]
