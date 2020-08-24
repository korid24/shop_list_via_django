# Generated by Django 3.1 on 2020-08-14 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0002_auto_20200812_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='index',
        ),
        migrations.RemoveField(
            model_name='purchaseslist',
            name='index',
        ),
        migrations.AddField(
            model_name='purchase',
            name='ind',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='Purchase index'),
        ),
        migrations.AddField(
            model_name='purchaseslist',
            name='ind',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='List index'),
        ),
    ]