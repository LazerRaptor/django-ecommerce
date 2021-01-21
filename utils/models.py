from django.db import models
from django.utils.text import slugify
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
           


