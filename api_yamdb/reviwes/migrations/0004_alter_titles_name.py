# Generated by Django 3.2 on 2023-11-15 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviwes', '0003_auto_20231115_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Произведение'),
        ),
    ]
