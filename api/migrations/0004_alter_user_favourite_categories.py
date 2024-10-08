# Generated by Django 4.2.6 on 2023-12-12 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_user_favourite_categories"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="favourite_categories",
            field=models.ManyToManyField(
                default=[], related_name="favourite_by", to="api.articlecategory"
            ),
        ),
    ]
