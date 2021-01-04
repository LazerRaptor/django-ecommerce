# Generated by Django 3.1.4 on 2020-12-23 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_remove_book_stockrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='title')),
                ('slug', models.SlugField(blank=True, editable=False, unique=True, verbose_name='slug')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='price')),
                ('description', models.TextField(blank=True, default='Description is not provided', verbose_name='description')),
                ('active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('bike_type', models.CharField(choices=[('R', 'Road bike'), ('C', 'Cruiser bike'), ('M', 'Mountain bike')], max_length=1, verbose_name="bike's type")),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bike_related', related_query_name='bike', to='catalog.category', verbose_name='related categories')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
