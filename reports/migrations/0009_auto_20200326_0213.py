# Generated by Django 2.2.11 on 2020-03-26 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0008_containertype_upload_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='containertype',
            name='material',
            field=models.CharField(max_length=50, verbose_name='Название'),
        ),
    ]
