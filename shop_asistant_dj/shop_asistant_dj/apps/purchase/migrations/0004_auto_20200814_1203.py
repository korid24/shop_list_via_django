# Generated by Django 3.1 on 2020-08-14 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0003_auto_20200814_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='ind',
            field=models.IntegerField(default=1000, verbose_name='Purchase index'),
        ),
        migrations.AlterField(
            model_name='purchaseslist',
            name='ind',
            field=models.IntegerField(default=1000, verbose_name='List index'),
        ),
    ]
