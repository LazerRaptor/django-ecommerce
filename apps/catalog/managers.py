from django.db import models 



class ProductManager(models.Manager):
    def slugs(self):
        return self.values_list('slug', flat=True)

    def featured(self):
        return self.filter(active=True).filter(featured=True)