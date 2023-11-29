# Generated by Django 4.2.7 on 2023-11-29 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("preferences", "__first__"),
        ("accounts", "0002_alter_user_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="preferences",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="preferences.preferences",
            ),
        ),
    ]
