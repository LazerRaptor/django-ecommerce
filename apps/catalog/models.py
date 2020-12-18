from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from .abstract_models import AbstractProduct
from utils.db.models import SlugFromTitleModel



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

    @property 
    def is_leaf_node(self):
        return self.is_leaf_node()



class Book(AbstractProduct):
    SOFT, HARD, EBOOK = 'S', 'H', 'E'
    BOOK_FORMAT_CHOICES = [
        (SOFT, _('soft cover')),
        (HARD, _('hard cover')),
        (EBOOK, _('eBook'))
    ]
    length = models.IntegerField(_('number of pages'))
    author = models.CharField(_('author'), max_length=255)
    book_format = models.CharField(_('book_format'), max_length=1, choices=BOOK_FORMAT_CHOICES)

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')
