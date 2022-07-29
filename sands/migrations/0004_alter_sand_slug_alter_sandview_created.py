# Generated by Django 4.0.6 on 2022-07-29 14:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sands', '0003_alter_sand_category_alter_sand_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sand',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='sandview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 29, 10, 39, 24, 532668)),
        ),
    ]