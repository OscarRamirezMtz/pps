# Generated by Django 3.2.19 on 2023-12-06 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20231206_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='backupconfig',
            name='server_origen',
        ),
    ]
