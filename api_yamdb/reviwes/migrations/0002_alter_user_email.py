# Generated by Django 3.2 on 2023-11-16 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviwes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='Электронная почта'),
        ),
    ]