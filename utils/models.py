from django.db import models
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _



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
    slug = AutoSlugField(
        _('slug'),
        populate_from=['title',],
        blank=True, 
        unique=True, 
        editable=False
    )

    class Meta: 
        abstract = True

    def __str__(self):
        return self.title

           


