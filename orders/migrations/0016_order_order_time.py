# Generated by Django 3.0 on 2019-12-11 08:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20191211_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
