from collections import deque
from typing import Type
from django.db import models
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured



class MergedQueryset(object):
    def __init__(self, model):
        if not model._meta.abstract:
            raise ImproperlyConfigured("Provided model must be abstract")
        self.model = model
        self.app_label = model._meta.app_label

    def _get_descendant_models(self):
        app_models = apps.get_app_config(self.app_label).get_models()
        child_models = (m for m in app_models if issubclass(m, self.model))
        return child_models
    
    def get_merged_queryset(self):
        fields = self.model._meta.get_fields() 
        field_names = [field.name for field in fields]
        child_models = list(self._get_descendant_models())
        queryset_list = []
        for model in child_models:
            qs = model.objects.values(*field_names)
            annotated_qs = qs.annotate(
                resource_model=models.Value(
                    self.model._meta.model_name,
                    models.CharField(max_length=120)
                )
            )
            queryset_list.append(annotated_qs)

        if len(queryset_list) > 1:
            merged_queryset = queryset_list[0].union(*queryset_list[1:])
        elif len(queryset_list) == 1:
            merged_queryset = queryset_list[0]
        else:
            merged_queryset = None 

        return merged_queryset
    


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

        self.all().delete()

        nodes, step = self._traverse(base_model)
        
        for node in nodes:
            self.create(**node)

    
    def get_merged_queryset(self, model: Type[models.Model]):
        '''
        Merge queryset of child concrete models for a given abstract model
        (base model by default). 
        '''
        fields = [field.name for field in model._meta.get_fields()]
        leaf_nodes = self.get_leaves(model)
        concrete_models = [node.get_model() for node in leaf_nodes]
        queryset_list = []
        for _model in concrete_models:
            qs = _model.objects.values(*fields)
            annotated_qs = qs.annotate(
                resource_model=models.Value(
                    _model._meta.model_name,
                    models.CharField(max_length=120)
                )
            )
            queryset_list.append(annotated_qs)

        if len(queryset_list) > 1:
            merged_queryset = queryset_list[0].union(*queryset_list[1:])
        elif len(queryset_list) == 1:
            merged_queryset = queryset_list[0]
        else:
            merged_queryset = None 

        return merged_queryset
    

    def get_root(self):
        return self.get(parent=None)
    

    def get_descendants(self, model: Type[models.Model]=None):
        if model is None:
            node = self.get_root()
        else: 
            node = self.get(app_label=model._meta.app_label, model_name=model._meta.model_name)
        descendants = self.filter(models.Q(lft__gt=node.lft) & models.Q(rgt__lt=node.rgt))
        return descendants
    

    def get_leaves(self, model: Type[models.Model]=None):   
        '''
        Leaf nodes correspond to concrete models
        '''
        return self.get_descendants(model).filter(rgt=models.F('lft') + 1)


    def _traverse(self, model, parent=None, step=0, nodes=[]):
        '''
        While traversing a class tree, create a dict for each class that will be used to 
        create Node instances. 
        '''
        step += 1
        node = {
            'app_label': model._meta.app_label,
            'model_name': model._meta.model_name,
            'lft': step,
            'rgt': None,
            'parent_id': parent['lft'] if parent is not None else None
        }

        subclasses = model.__subclasses__()

        for subclass in subclasses: 
            nodes, step = self.traverse(
                model=subclass,
                parent=node,
                step=step,
                nodes=nodes
            )

        step += 1
        node['rgt'] = step 
        nodes.append(node)
        return nodes, step