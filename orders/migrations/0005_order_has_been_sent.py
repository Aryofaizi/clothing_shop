# Generated by Django 5.0.4 on 2024-04-17 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_post_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='has_been_sent',
            field=models.BooleanField(default=False),
        ),
    ]
