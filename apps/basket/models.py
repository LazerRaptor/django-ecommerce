import uuid
from django.db import models
from django.conf import settings
from utils.models import TimeStampedModel



User = settings.AUTH_USER_MODEL


class Basket(TimeStampedModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

def __str__(self):
    return str(self.id)