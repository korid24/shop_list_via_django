# Generated by Django 3.1 on 2020-08-14 07:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0004_auto_20200814_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='creation_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation time'),
        ),
        migrations.AlterField(
            model_name='purchaseslist',
            name='creation_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation time'),
        ),
    ]