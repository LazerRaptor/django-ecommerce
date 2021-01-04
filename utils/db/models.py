from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from collections import deque
from typing import Type



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


class TreeManager(models.Manager):
    def rebuild(self, base_model: Type[models.Model]) -> None:
        '''
        Creates a tree representation for a class hierarchy.
        base_model argument should be a subclass of Django's Model class. 
        It becomes the root node for the tree, from there we drill down to its leaves 
        (that are supposedly concrete models, unlike root and branch nodes).
        '''
        assert issubclass(base_model, models.Model), (
            f'{base_model} is not a model'
        )
        
        # clear tree
        self.all().delete()

        queue = deque([
            (base_mode, None)
        ])
        
        self._traverse(queue)


    def _traverse(self, queue: deque) -> None:
        try:
            model, parent_node = queue.pop()
        except IndexError:
            print('Tree traversal complete')
        
        node, created = self.get_or_create(
            app_label=model._meta.app_label,
            model_name=model._meta.model_name,
            parent=parent_node
        )
        for subclass in model.__subclasses__():
            queue.append(
                (subclass, node)
            )
            self._traverse(queue)



class Node(models.Model):
    model_name = models.CharField(_('model\'s name'), max_length=120)
    app_label = models.CharField(_('application\'s label'), max_length=120)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name="children", 
        verbose_name=_('parent')
    )
    objects = TreeManager()

    class Meta:
        abstract = True
        unique_together = ['model_name', 'app_label']

    def __str__(self):
        return f'{self.app_label} | {self.model_name}'


