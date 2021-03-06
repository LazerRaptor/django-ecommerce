import uuid
from django.db import models
from django.conf import settings
from utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

from catalog.models import Product


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
    OPEN, SUBMITTED = ('open', 'submitted')
    STATUS_CHOICES = (
        (OPEN, _('Open - active basket')),
        (SUBMITTED, _('Submitted - items has been purchased'))
    )
    status = models.CharField(
        _('Status'), 
        max_length=15, 
        default='open', 
        choices=STATUS_CHOICES
    )

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')

    def __str__(self):
        return str(self.id)
    
    def add(self, product_id, quantity = 1):
        '''
        Add product to the basket.
        '''
        if Product.objects.filter(id=product_id).exists():
            instance = BasketLine.objects.create(
                basket_id = self.id,
                product_id = product_id,
                quantity = quantity
            )
            return instance
        else: 
            pass

    def remove(self, line_id):
        try:
            instance = BasketLine.objects.get(id=line_id)
            instance.delete()
        except BasketLine.DoesNotExist:
            pass 


class BasketLine(models.Model):
    '''
    Represents items of same product type in basket.
    '''
    basket = models.ForeignKey(
        'basket.Basket',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('basket')
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('product')
    )
    quantity = models.PositiveIntegerField(_('quantity'), default=1)

    class Meta: 
        verbose_name = _('Basket Line')
        verbose_name_plural = _('Basket Lines')
        unique_together = ('basket', 'product')
    
    def __str__(self):
        return f'{self.product.title} ({self.quantity})'