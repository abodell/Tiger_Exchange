# Generated by Django 4.1.7 on 2023-03-12 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='cart',
            field=models.ManyToManyField(blank=True, to='my_app.cart'),
        ),
    ]
