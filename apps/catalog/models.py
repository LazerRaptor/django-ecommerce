from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from utils.models import TimeStampedModel, SlugFromTitleModel
from .managers import ProductManager



class Category(SlugFromTitleModel, MPTTModel):
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='children',
        verbose_name=_('parent')
    )

    class Meta: 
        verbose_name = _('category')
        verbose_name_plural = _('categories')
    
    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['title']

    def __str__(self):
        return self.title



class Product(TimeStampedModel, SlugFromTitleModel):
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
    extra = models.JSONField(_('extra attributes as JSON'), null=True, blank=True)
    objects = ProductManager()

