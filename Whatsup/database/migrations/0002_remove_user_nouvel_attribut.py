# Generated by Django 3.2.18 on 2023-12-18 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='nouvel_attribut',
        ),
    ]
