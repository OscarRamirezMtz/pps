# Generated by Django 3.2.19 on 2023-12-20 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_remove_backupconfig_server_origen'),
    ]

    operations = [
        migrations.AddField(
            model_name='backupconfig',
            name='server_remitente',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='respaldos_remitente', to='backend.server1'),
        ),
    ]
