# Generated by Django 3.2.7 on 2021-09-25 07:18

import apps.stores.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='food_img',
            field=models.ImageField(upload_to=apps.stores.models.set_food_img_path, verbose_name='식자재 사진'),
        ),
        migrations.AlterField(
            model_name='food',
            name='receipt',
            field=models.ImageField(upload_to=apps.stores.models.set_receipt_img_path, verbose_name='영수증'),
        ),
    ]
