# Generated by Django 3.2 on 2023-11-15 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviwes', '0008_alter_titles_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='titles',
            name='description',
            field=models.TextField(default='qq'),
            preserve_default=False,
        ),
    ]