# Generated by Django 3.0.14 on 2023-07-10 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20230710_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='intro',
            field=models.CharField(max_length=550),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]