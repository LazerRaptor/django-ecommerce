# Generated by Django 3.1.6 on 2021-03-06 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        ('basket', '0003_basketline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketline',
            name='basket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='basket.basket', verbose_name='basket lines'),
        ),
        migrations.AlterUniqueTogether(
            name='basketline',
            unique_together={('basket', 'product')},
        ),
    ]