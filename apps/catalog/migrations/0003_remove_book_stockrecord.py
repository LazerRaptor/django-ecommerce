# Generated by Django 3.1.4 on 2020-12-18 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20201216_0245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='stockrecord',
        ),
    ]
