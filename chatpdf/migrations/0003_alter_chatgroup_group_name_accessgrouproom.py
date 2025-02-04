# Generated by Django 5.0.6 on 2024-07-01 09:14

import django.db.models.deletion
import shortuuid.main
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatpdf', '0002_alter_chatgroup_group_name_alter_groupmessage_group'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='group_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True),
        ),
        migrations.CreateModel(
            name='AccessGroupRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(blank=True, default='', max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
