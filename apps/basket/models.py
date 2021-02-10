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
        related_name='baskets',
        verbose_name=_('owner')
    )
    products = models.ManyToManyField(
        'catalog.Product',
        through='ProductArray',
        through_fields=('basket', 'product'),
        verbose_name=_('products')
    )
    OPEN, SUBMITTED = ('open', 'submitted')
    STATUS_CHOICES = (
        (OPEN, _('Open - active basket')),
        (SUBMITTED, _('Submitted - items has been purchased'))
    )
    status = models.CharField(
        _('Status'), max_length=15, default='open', choices=STATUS_CHOICES
    )

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')

    def __str__(self):
        return str(self.id)


    
class ProductArray(TimeStampedModel):
    '''
    Through model for ManyToMany relationship between
    Product (target) and Basket (source) models. Represents
    a number of same products added to a basket.
    '''
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        verbose_name=_('product')
    )
    basket = models.ForeignKey(
        'basket.Basket', 
        on_delete=models.CASCADE,
        verbose_name=_('basket')
    )
    quantity = models.PositiveIntegerField(_('quantity'), default=1)

    def __str__(self):
        return f'{self.product} ({self.quantity})'