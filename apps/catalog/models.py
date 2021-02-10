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
        related_name='products',
        verbose_name = _('related categories')
    )
    extra = models.JSONField(_('extra attributes as JSON'), null=True, blank=True)
    objects = ProductManager()

    def __str__(self):
        return self.title



def build_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/images/<product_title>/<filename>
    return 'uploads/images/{0}/{1}'.format(instance.product.title, filename)



class ProductImage(models.Model):
    src = models.ImageField(
        _('source'),
        upload_to=build_image_path, 
        unique=True,
        help_text=_('Image file that will be available via URL after upload')
    )
    product = models.ForeignKey(
        'catalog.Product', 
        related_name='images', 
        on_delete=models.CASCADE, 
        verbose_name=_('product')
    )
    alt = models.CharField(
        _('image description'),
        max_length=255, 
        null=True, 
        blank=True,
        help_text=_('It\'s used as plain text when image is not shown')
    )
    is_showcase = models.BooleanField(
        _('is showcase'), 
        default=False, 
        help_text=_('This image is for showcase purposes and should be unique per product')
    )

    class Meta:
        verbose_name=_('Product Image')
        verbose_name_plural=_('Product Images')

    def __str__(self):
        return f'{self.product.title} ({self.id})' 
    



