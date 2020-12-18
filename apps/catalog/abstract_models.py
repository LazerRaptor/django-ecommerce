from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from utils.db.models import TimeStampedModel, SlugFromTitleModel
from django.utils.translation import gettext_lazy as _
from warehouse.models import StockRecord



class AbstractProduct(TimeStampedModel, SlugFromTitleModel):
    price = models.DecimalField(_('price'), max_digits=12, decimal_places=2)
    description = models.TextField(_('description'), blank=True, default='Description is not provided')
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(
        'catalog.Category', 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='%(class)s_related',
        related_query_name='%(class)s',
        verbose_name = _('related categories')
    )
    stockrecords = GenericRelation(
        StockRecord,
        related_query_name='%(class)s',
        verbose_name=_('stock records')
    )

    class Meta: 
        abstract = True





