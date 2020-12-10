from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _



class StatusModel(models.Model):
    '''
    Abstract model with timestamp and state fields.
    '''
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    active = models.BooleanField(_('active'), default=True)
    featured = models.BooleanField(_('featured'), default=False)

    class Meta:
        abstract = True



class TitleDescriptionModel(models.Model):
    '''
    Abstract model with title, description, and "auto-slug" field.  
    '''
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), blank=True, unique=True, editable=False)
    description = models.TextField(_('description'), blank=True, default='No description provided.')

    class Meta: 
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)