from collections import deque
from typing import Type, List
from itertools import chain
from django.db import models
from django.db import connection
from psycopg2 import sql
from utils.decorators import timeit


class TreeManager(models.Manager):
    def rebuild(self) -> None:
        '''
        Creates a tree representation for a class hierarchy.
        base_model corresponds to a root node of the tree. 
        '''

        base_model = self.model._tree_meta.base_model

        self.all().delete()

        objects, step = self._traverse(base_model)
        
        # TODO: try bulk create instead
        for obj in objects:
            self.create(**obj)


    def dictfetchall(self, cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    @timeit
    def fetchall(self, **kwargs):
        ''' 
        We can perform filtering by using Q object, like so:
        query = Q()
        for key, value in kwargs.items():
            query &= Q(key=value)
        rows = rows.filter(query)
        '''
        base = self.model._tree_meta.base_model
        fields = self._get_fields(base)
        nodes = self.get_leaves()
        qs = None
    
        for node in nodes:
            model = node.get_model()
            qs1 = model.objects.values(*fields)
            qs = qs.union(qs1) if qs is not None else qs1 

        return qs

    @timeit 
    def get_union(self):
        base = self.model._tree_meta.base_model
        fields = self._get_fields(base)
        leaves = self.get_leaves()
        qs_list = []

        for leaf in leaves:
            model = leaf.get_model()
            rows = model.objects.values(*fields)
            qs_list.append(rows)
        
        qs = qs_list[0].union(*qs_list[1:])
        return qs


    @timeit
    def raw_sql(self, model: Type[models.Model]=None):
        '''
        Merge queryset of child concrete models of a given abstract model
        (base model by default). 
        '''
        if model is None:
            model = self.model._tree_meta.base_model
        
        leaves = self.get_leaves(model)
        db_tables = [leaf.get_model()._meta.db_table for leaf in leaves]
        columns = self._get_column_names(model)
        data = []

        with connection.cursor() as cursor:
            for table in db_tables:
                query = sql.SQL("SELECT {cols} FROM {table}").format(
                    cols=sql.SQL(', ').join(
                        [sql.Identifier(col) for col in columns]
                    ),
                    table=sql.Identifier(table)
                )
                cursor.execute(query)
                rows = self.dictfetchall(cursor)
                data = list(chain(data, rows))

        return data

    

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


    def _get_column_names(self, model):
        '''
        Get db column names to perform raw queries.
        '''
        fields = model._meta.fields
        col_names = []

        for field in fields:
            field_name, column_name = field.get_attname_column()
            col_names.append(column_name)
        
        return col_names


    def _get_fields(self, model):
        return [
            field.name for field in model._meta.get_fields()
        ]

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