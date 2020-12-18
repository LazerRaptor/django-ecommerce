from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from utils.db.models import SlugFromTitleModel, TimeStampedModel



class Supplier(models.Model):
    '''
    Concrete model that describes suppliers.
    '''
    pass


class StockRecordManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def stocked(self):
        '''
        Queryset of product models' instances whose cumulative delta of 
        related stockrecords is positive.  
        '''
        pass 

    def out_of_stock(self):
        pass
    
    def check_availability(self, name):
        pass


class StockRecord(TimeStampedModel):
    '''
    Concrete model that holds information about restocking and realization of products. 
    '''
    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.CASCADE,
        null = True,
        blank = True,
        verbose_name=_('supplier')
    )
    basket = models.ForeignKey(
        'basket.Basket',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('basket')
    )
    # Generic relationship to AbstractProduct model's children
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('content type')
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    delta = models.IntegerField(
        _('delta'), 
        help_text=_(
            'Positive and negative deltas mean restocking and realization respectively'
        )
    )

    class Meta:
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
        return f'{self.delta} of {self.product}'





 