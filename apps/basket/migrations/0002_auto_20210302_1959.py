# Generated by Django 3.1.6 on 2021-03-02 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='products',
        ),
        migrations.DeleteModel(
            name='ProductArray',
        ),
    ]