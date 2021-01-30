import uuid
from django.db import models
from django.conf import settings
from utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


User = settings.AUTH_USER_MODEL


class Basket(TimeStampedModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('owner')
    )
    OPEN, SAVED, SUBMITTED = (
        'Open', 'Saved', 'Submitted'
    )
    STATUS_CHOICES = (
        (OPEN, _('Open - active basket')),
        (SAVED, _('Saved for later')),
        (SUBMITTED, _('Submitted - items has been purchased'))
    )
    status = models.CharField(
        _('Status'), max_length=15, default='Open', choices=STATUS_CHOICES
    )

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')

    def __str__(self):
        return str(self.id)