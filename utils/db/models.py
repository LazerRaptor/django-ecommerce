from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from collections import deque

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



class NodeTreeManager(TreeManager):
    def rebuild_tree(self, base_model):
        '''
        Creates a tree representation for a class hierarchy.
        base_model argument should be a subclass of Django's Model class. 
        It becomes the root node for the tree, from there we drill down to its leaves 
        (that are supposedly concrete models, unlike root and branch nodes).
        '''
        assert issubclass(base_model, models.Model), (
            f'{base_model} is not a model'
        )

        # TODO
        if self.is_sync():
            return

        # delete all
        self.all().delete()

        queue = deque()
        parent = base_model
        children = parent.__subclasses__()

        rv = deque()

        # init the root node
        try:
            root, created = self.get_or_create(
                app_label=parent._meta.app_label,
                model_name=parent._meta.model_name
            )
            rv.append(root)
        except:
            print("Something is wrong again :(")
        
        queue.append(
            (parent, root, children)
        )

        # start to drill down
        while len(queue) > 0:
            parent, parent_obj, children = queue.pop()
            
            for child in children:
                node = self._update_or_create(subclass=child, parent_obj=parent_obj)
                if child.__subclasses__():
                    queue.append(
                        (child, node, child.__subclasses__())
                    )
                rv.append(node)

        return rv
            

    def _update_or_create(self, subclass, parent_obj):
        node, created = self.get_or_create(
            app_label=subclass._meta.app_label,
            model_name=subclass._meta.model_name,
            parent = parent_obj
        )
        return node

    def _remove_obsolete_nodes(self):
        pass


    def is_sync(self):
        pass



class Node(MPTTModel):
    model_name = models.CharField(_('model\'s name'), max_length=120)
    app_label = models.CharField(_('application\'s label'), max_length=120)
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name="children", 
        verbose_name=_('parent')
    )
    objects = NodeTreeManager()

    class Meta:
        abstract = True
        unique_together = ['model_name', 'app_label']


    class MPTTMeta:
        level_attr = 'mptt_level'


    def __str__(self):
        return f'{self.app_label} | {self.model_name}'


