# Generated by Django 5.2.1 on 2025-05-31 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motos', '0008_alter_moto_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moto',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='motos/%Y/', verbose_name='Photo de la moto'),
        ),
    ]
