# Generated by Django 2.1.3 on 2018-11-23 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_movie_imdbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='released',
            field=models.DateField(null=True),
        ),
    ]
