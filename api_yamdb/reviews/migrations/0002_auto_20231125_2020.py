# Generated by Django 3.2 on 2023-11-25 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('name',), 'verbose_name': 'жанр', 'verbose_name_plural': 'жанры'},
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
    ]
