# Generated by Django 5.1.6 on 2025-03-04 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_code_consumed_at_alter_code_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
