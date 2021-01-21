from django.db.models.base import ModelBase
from django.contrib.contenttypes.models import ContentType
from .managers import TreeManager



class TreeOptions:
    base_model = None

    def __init__(self, options, **kwargs):
        if options:
            options = list(options.__dict__.items())
        else: 
            options = []

        options.extend(list(kwargs.items()))

        for key, value in options:
            if key[:2] == '__':
                continue
            setattr(self, key, value)



class TreeModelBase(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        super_new = super().__new__
        TreeMeta = attrs.pop('TreeMeta', None)

        if TreeMeta is None:
            class TreeMeta:
                pass

        attrs['_tree_meta'] = TreeOptions(TreeMeta)

        return super_new(cls, name, bases, attrs)


class Node(models.Model, metaclass=TreeModelBase):
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


