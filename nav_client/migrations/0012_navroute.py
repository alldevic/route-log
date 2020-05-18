# Generated by Django 2.2.12 on 2020-05-12 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nav_client', '0011_auto_20200420_0652'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nav_id', models.IntegerField(verbose_name='nav_id')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('from_utc', models.CharField(max_length=150, verbose_name='from_utc')),
                ('to_utc', models.CharField(max_length=150, verbose_name='to_utc')),
                ('nav_device_id', models.IntegerField(verbose_name='nav_device_id')),
                ('nav_driver_id', models.IntegerField(verbose_name='nav_driver_id')),
                ('sync_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='nav_client.SyncDate', verbose_name='дата синхронизации')),
            ],
            options={
                'verbose_name': 'маршрут навигации',
                'verbose_name_plural': 'маршруты навигации',
            },
        ),
    ]
