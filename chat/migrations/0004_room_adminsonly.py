# Generated by Django 4.2.7 on 2023-11-30 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0003_alter_room_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="adminsOnly",
            field=models.BooleanField(default=False),
        ),
    ]
