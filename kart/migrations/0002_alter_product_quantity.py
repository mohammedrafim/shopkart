# Generated by Django 3.2.14 on 2022-12-25 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
