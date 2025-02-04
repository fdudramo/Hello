# Generated by Django 5.0.6 on 2024-06-12 01:50

import django.db.models.deletion
import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatpdf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='group_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='groupmessage',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to='chatpdf.chatgroup'),
        ),
    ]
