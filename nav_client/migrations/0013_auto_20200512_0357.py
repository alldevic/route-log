# Generated by Django 2.2.12 on 2020-05-12 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nav_client', '0012_navroute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navroute',
            name='from_utc',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='from_utc'),
        ),
        migrations.AlterField(
            model_name='navroute',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='navroute',
            name='nav_device_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='nav_device_id'),
        ),
        migrations.AlterField(
            model_name='navroute',
            name='nav_driver_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='nav_driver_id'),
        ),
        migrations.AlterField(
            model_name='navroute',
            name='to_utc',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='to_utc'),
        ),
    ]
