# Generated by Django 5.0.4 on 2024-04-13 07:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rate', models.IntegerField(choices=[(5, 'EXCELLENT'), (4, 'GOOD'), (3, 'NOT BAD'), (2, 'BAD'), (1, 'VERY BAD')])),
                ('status', models.CharField(choices=[('w', 'Waiting'), ('a', 'Approved'), ('na', 'Not Approved')], default='w', max_length=2)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
