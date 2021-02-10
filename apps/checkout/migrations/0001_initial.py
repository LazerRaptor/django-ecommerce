# Generated by Django 3.1.6 on 2021-02-09 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import django_lifecycle.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basket', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=12, unique=True, verbose_name='order number')),
                ('status', models.CharField(choices=[('created', 'Order created'), ('progress', 'Order is accepted and being processed'), ('completed', 'Order is completed'), ('cancelled', 'Order has been cancelled and is waiting for refund'), ('refunded', 'Order has been refunded')], max_length=120, verbose_name='status')),
                ('basket', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basket.basket', verbose_name='basket')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='customer')),
            ],
            options={
                'abstract': False,
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
