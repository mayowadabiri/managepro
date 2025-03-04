# Generated by Django 5.1.6 on 2025-03-03 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages='A user with the email address already exists', max_length=254, unique=True),
        ),
    ]
