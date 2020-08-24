# Generated by Django 3.1 on 2020-08-20 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20200820_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramsession',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='telegtam_session', to=settings.AUTH_USER_MODEL),
        ),
    ]
