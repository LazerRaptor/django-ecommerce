from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from .managers import TreeManager
from .exceptions import NotConcreteModel


class TimeStampedModel(models.Model):
    '''
    Abstract model with created and updated auto fields.
    '''
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        abstract = True



class SlugFromTitleModel(models.Model):
    '''
    Abstract model with title, description, and "auto-slug" field.  
    '''
    title = models.CharField(_('title'), max_length=255, unique=True)
    slug = models.SlugField(_('slug'), blank=True, unique=True, editable=False)

    class Meta: 
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # TODO: is it ok? 
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)







class Node(models.Model):
    '''
    Notice that 'lft' attribute is used as a primary key. This is potentially bad if we decide to 
    expand the functionality.  
    '''
    model_name = models.CharField(_('model\'s name'), max_length=120)
    app_label = models.CharField(_('application\'s label'), max_length=120)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name="children", 
        verbose_name=_('parent'),
        editable=False
    )
    lft = models.PositiveIntegerField(_('left'), primary_key=True, editable=False)
    rgt = models.PositiveIntegerField(_('right'), unique=True, editable=False)
    objects = TreeManager()


    class Meta:
        abstract = True
        unique_together = ['model_name', 'app_label']


    def __str__(self):
        return f'{self.app_label} | {self.model_name}'


    def get_model(self):
        ct = ContentType.objects.get(
            app_label=self.app_label, model=self.model_name)
        return ct.model_class()


    @property
    def is_root(self):
        return self.parent is None


    @property
    def is_leaf(self):
        return self.rgt - self.lft == 1


