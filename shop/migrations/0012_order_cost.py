# Generated by Django 3.0.14 on 2023-07-03 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20230627_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]
