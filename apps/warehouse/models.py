from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import SlugFromTitleModel, TimeStampedModel



class StockRecordManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def stocked(self):
        '''
        Get all instances related to one product, filter by cumulative delta > 0 
        '''
        pass
    
    def out_of_stock(self):
        pass


class StockRecord(SlugFromTitleModel, TimeStampedModel):
    '''
    Holds information about restocking and realization of products. 
    '''
    delta = models.IntegerField(
        _('delta'), 
        helper_text=_(
            'Positive and negative deltas mean restocking and realization respectively'
        )
    )
    basket = models.ForeignKey(
        'basket.Basket',
        on_delete=models.CASCADE,
        verbose_name=_('basket')
    )