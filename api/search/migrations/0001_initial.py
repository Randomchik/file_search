# Generated by Django 5.1.2 on 2024-10-28 17:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(blank=True, max_length=255, null=True)),
                ('file_mask', models.CharField(blank=True, max_length=255, null=True)),
                ('size_value', models.BigIntegerField(blank=True, null=True)),
                ('size_operator', models.CharField(blank=True, max_length=2, null=True)),
                ('creation_time_value', models.DateTimeField(blank=True, null=True)),
                ('creation_time_operator', models.CharField(blank=True, max_length=2, null=True)),
                ('finished', models.BooleanField(default=False)),
                ('results', models.JSONField(default=list)),
            ],
        ),
    ]
