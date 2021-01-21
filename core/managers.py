from collections import deque
from typing import Type, List
from django.db import models
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured



class TreeManager(models.Manager):
    def rebuild(self) -> None:
        '''
        Creates a tree representation for a class hierarchy.
        base_model argument should be a subclass of Django's Model class. 
        It becomes the root node for the tree, from there we drill down to its leaves 
        (that are supposedly concrete models, unlike root and branch nodes).
        '''

        base_model = self.model._tree_meta.base_model

        self.all().delete()

        nodes, step = self._traverse(base_model)
        
        for node in nodes:
            self.create(**node)

    
    def get_merged_queryset(self, model: Type[models.Model]):
        '''
        Merge queryset of child concrete models of a given abstract model
        (base model by default). 
        '''
        fields = [field.name for field in model._meta.get_fields()]
        leaf_nodes = self.get_leaves(model)
        concrete_models = [node.get_model() for node in leaf_nodes]
        qs_list = [
            c_model.objects.values(*fields) for c_model in concrete_models
        ]   
        merged_queryset = qs_list.pop()
        while len(qs_list) > 0:
            merged_queryset.union(qs_list.pop())
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