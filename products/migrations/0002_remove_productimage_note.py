# Generated by Django 3.1.2 on 2020-10-25 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='note',
        ),
    ]
