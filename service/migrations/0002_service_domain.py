# Generated by Django 5.1.6 on 2025-03-05 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='domain',
            field=models.URLField(max_length=100, null=True),
        ),
    ]
