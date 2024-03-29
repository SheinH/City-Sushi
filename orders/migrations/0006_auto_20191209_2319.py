# Generated by Django 3.0 on 2019-12-09 23:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_delivery_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dish_name',
        ),
        migrations.AddField(
            model_name='visitor',
            name='phone',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='orders.Dish')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
            ],
        ),
    ]
