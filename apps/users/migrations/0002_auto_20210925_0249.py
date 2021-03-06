# Generated by Django 3.2.7 on 2021-09-25 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='long',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.address', verbose_name='주소'),
        ),
    ]
