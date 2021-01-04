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
    
