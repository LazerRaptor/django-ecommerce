from django.db import models 
from django.contrib.contenttypes.models import ContentType



class ProductManager(models.Manager):
    def slugs(self):
        return self.values_list('slug', flat=True)

    def featured(self):
        return self.filter(active=True).filter(featured=True)

    def create_many(self, object_list: list):
        '''
        Create multiple objects from a list of dictionaries
        '''
        instance_list = [self.model(**obj) for obj in object_list]
        self.bulk_create(instance_list)
    
    
    # silly methods for populating the model with dummy data
    
    def populate_dummy(self, object_list: list):
        objs = [self._mutate_obj(obj) for obj in object_list]
        self.create_many(objs)
    
    def _mutate_obj(self, obj: dict):
        '''
        Replace 'category': str(val) with 'category_id': int(id)
        '''
        title = obj.pop('category')
        model = ContentType.objects.get(app_label='catalog', model='category').model_class()
        cat_obj = model.objects.get(title__iexact=title)
        obj['category_id'] = cat_obj.id
        return obj

