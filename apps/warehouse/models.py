from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import TimeStampedModel



class Supplier(models.Model):
    '''
    Concrete model that describes suppliers.
    '''
    title = models.CharField(_('title'), max_length=127)
    address = models.CharField(_('address'), max_length=255)

    class Meta: 
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')

    def __str__(self):
        return self.title



class StockRecord(TimeStampedModel):
    '''
    Concrete model that holds information about restocking and realization of products. 
    '''
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        null = True,
        blank = True,
        related_name='stockrecords',
        verbose_name=_('supplier')
    )
    basket = models.ForeignKey(
        'basket.Basket',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='stockrecords',
        verbose_name=_('basket')
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        related_name='stockrecords',
        verbose_name=_('product')
    )
    delta = models.IntegerField(
        _('delta'), 
        help_text=_(
            'Positive and negative deltas mean restocking and realization respectively'
        )
    )

    class Meta:
        verbose_name = _('Stock Record')
        verbose_name_plural = _('Stock Records')
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(
                        basket__isnull=True,
                        supplier__isnull=False,
                        delta__gt=0
                    ) | models.Q(
                        basket__isnull=False,
                        supplier__isnull=True,
                        delta__lt=0
                    )
                ),
                name='mutual_exclusion'
            ),
        ]

    def __str__(self):
        return f'{self.content_object} ({self.delta})'







 