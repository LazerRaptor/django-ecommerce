import uuid
from django.db import models
from django.conf import settings
from utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


User = settings.AUTH_USER_MODEL


class Basket(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('owner')
    )
    products = models.ManyToManyField(
        'catalog.Product',
        through='BasketProduct',
        through_fields=('basket', 'product'),
        verbose_name=_('products')
    )
    OPEN, SAVED, SUBMITTED = (
        'open', 'saved', 'submitted'
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


    
class BasketProduct(TimeStampedModel):
    '''
    Through model for ManyToMany relationship between
    Product (target) and Basket (source) models. 
    '''
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        verbose_name=_('product')
    )
    basket = models.ForeignKey(
        'Basket', 
        on_delete=models.CASCADE,
        verbose_name=_('basket')
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product} ({self.quantity})'