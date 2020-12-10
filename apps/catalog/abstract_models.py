from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.db.models import StatusModel, TitleDescriptionModel



class AbstractProduct(StatusMode, TitleDescriptionModel, models.Model):
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta: 
        abstract = True