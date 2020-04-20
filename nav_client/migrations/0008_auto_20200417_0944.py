# Generated by Django 2.2.12 on 2020-04-17 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nav_client', '0007_merge_20200316_0205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customgeozone',
            options={'verbose_name': 'спец. зона', 'verbose_name_plural': 'спец. зоны'},
        ),
        migrations.AddField(
            model_name='customgeozone',
            name='sync_date',
            field=models.ForeignKey(default=113, on_delete=django.db.models.deletion.CASCADE, related_name='customgeozones', to='nav_client.SyncDate', verbose_name='дата синхронизации'),
        ),
    ]