# Generated by Django 4.2.6 on 2023-12-12 21:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_alter_user_favourite_categories"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="articlecomment",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
