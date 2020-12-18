# Generated by Django 3.1.4 on 2020-12-16 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='title')),
                ('slug', models.SlugField(blank=True, editable=False, unique=True, verbose_name='slug')),
                ('delta', models.IntegerField(help_text='Positive and negative deltas mean restocking and realization respectively', verbose_name='delta')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
