from django.db import models
from django_extensions.db.fields import RandomCharField
from django.utils.translation import gettext_lazy as _



class Order(models.Model):
    uuid = models.RandomCharField(_('order number'), length=12, unique=True)
    CREATED, IN_PROGRESS, COMPLETED = ('created', 'progress', 'completed')
    STATUS_CHOICES = (
        (CREATED, _('Order created')),
        (IN_PROGRESS, _('Order is accepted and being processed')),
        (COMPLETED, _('Order is completed'))
    )
    status = models.CharField(_('status'), max_length=120, choices=STATUS_CHOICES)
