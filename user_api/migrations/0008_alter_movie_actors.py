# Generated by Django 5.0.4 on 2024-05-01 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_api', '0007_rename_score_movie_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actors',
            field=models.CharField(max_length=1024),
        ),
    ]
