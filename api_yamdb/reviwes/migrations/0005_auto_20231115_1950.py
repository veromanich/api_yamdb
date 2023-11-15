# Generated by Django 3.2 on 2023-11-15 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviwes', '0004_alter_titles_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-id'], 'verbose_name': 'категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(max_length=256, unique=True, verbose_name='Идентификатор'),
        ),
    ]