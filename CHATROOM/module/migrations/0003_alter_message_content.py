# Generated by Django 5.1.1 on 2025-01-05 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0002_alter_user_avatar_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(null=True, verbose_name='Message Content'),
        ),
    ]
