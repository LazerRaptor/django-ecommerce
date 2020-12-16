from django.db import models
from utils.db.models import TimeStampedModel, SlugFromTitleModel
from django.utils.translation import gettext_lazy as _



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
    stockrecord = models.OneToOneField(
        'warehouse.StockRecord',
        on_delete=models.SET_NULL,
        null=True,
        related_name='product',
        verbose_name=_('stock record')
    )

    class Meta: 
        abstract = True





