# Generated by Django 3.0.6 on 2020-08-12 09:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(default=1000, verbose_name='Purchase index')),
                ('title', models.CharField(max_length=20, verbose_name='Purchase title')),
                ('creation_time', models.DateField(default=django.utils.timezone.now, verbose_name='Creation time')),
            ],
        ),
        migrations.CreateModel(
            name='PurchasesList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(default=1000, verbose_name='List index')),
                ('title', models.CharField(max_length=20, verbose_name='List title')),
                ('creation_time', models.DateField(default=django.utils.timezone.now, verbose_name='Creation time')),
                ('last_change', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last change')),
                ('lenght', models.IntegerField(default=0, verbose_name='List lenght')),
            ],
        ),
    ]