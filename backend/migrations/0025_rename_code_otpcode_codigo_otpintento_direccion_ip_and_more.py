# Generated by Django 5.2 on 2025-05-26 00:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_rename_otpattempt_otpintento'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='otpcode',
            old_name='code',
            new_name='codigo',
        ),
        migrations.AddField(
            model_name='otpintento',
            name='direccion_ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='otpintento',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otp_attempts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='otpintento',
            unique_together={('user', 'direccion_ip')},
        ),
    ]
