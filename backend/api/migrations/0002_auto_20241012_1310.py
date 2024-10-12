# Generated by Django 5.1 on 2024-08-30 19:51

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def init_data(apps, schema_editor):
    User = apps.get_model("auth", "User")

    # Create superuser
    if not User.objects.filter(username=settings.ADMIN_USERNAME):
        user = User(username=settings.ADMIN_USERNAME)
        user.password = make_password(settings.ADMIN_PASSWORD)
        user.is_staff = True
        user.is_superuser = True
        user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(init_data, migrations.RunPython.noop),
    ]
