# Generated by Django 2.1.3 on 2018-11-23 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_auto_20181123_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='imdbID',
            field=models.CharField(default='', max_length=20, unique=True),
            preserve_default=False,
        ),
    ]