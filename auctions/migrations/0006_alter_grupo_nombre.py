# Generated by Django 5.0.2 on 2024-02-24 03:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_grupo_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='nombre',
            field=models.CharField(default=uuid.uuid1, max_length=64, unique=True),
        ),
    ]