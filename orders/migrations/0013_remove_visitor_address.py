# Generated by Django 3.0 on 2019-12-10 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20191210_2330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitor',
            name='address',
        ),
    ]