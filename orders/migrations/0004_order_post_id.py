# Generated by Django 5.0.4 on 2024-04-17 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='post_id',
            field=models.CharField(default=664343452, max_length=12),
            preserve_default=False,
        ),
    ]
