# Generated by Django 5.0.2 on 2024-02-24 13:06

import auctions.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_grupo_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivos',
            name='archivo',
            field=models.FileField(upload_to=auctions.models.user_directory_path),
        ),
    ]
