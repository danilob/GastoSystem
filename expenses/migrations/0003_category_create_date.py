# Generated by Django 3.2 on 2022-07-13 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_payment_create_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='create_date',
            field=models.DateField(auto_now=True, verbose_name='Data de Criação'),
        ),
    ]
