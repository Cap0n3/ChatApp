# Generated by Django 4.2.7 on 2023-11-30 13:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chat", "0004_room_adminsonly"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatserver",
            name="admins",
            field=models.ManyToManyField(
                blank=True, related_name="admins", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]