# Generated by Django 5.0.4 on 2024-06-19 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_orderitem_color_orderitem_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='total',
            field=models.PositiveIntegerField(default=123),
            preserve_default=False,
        ),
    ]
