from django.db import models
from django.conf import settings
from django_extensions.db.fields import RandomCharField
from django.utils.translation import gettext_lazy as _
from django_lifecycle import (
    LifecycleModel, hook, AFTER_CREATE, AFTER_UPDATE)
from warehouse.models import StockRecord


User = settings.AUTH_USER_MODEL


class Order(LifecycleModel):
    '''
    
    '''
    uuid = RandomCharField(_('order number'), length=12, unique=True)
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name=_('customer')
    )
    basket = models.OneToOneField(
        'basket.Basket',
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name=_('basket')
    )
    CREATED, IN_PROGRESS, COMPLETED, CANCELLED, REFUNDED = (
        'created', 'progress', 'completed', 'cancelled', 'refunded')
    STATUS_CHOICES = (
        (CREATED, _('Order created')),
        (IN_PROGRESS, _('Order is accepted and being processed')),
        (COMPLETED, _('Order is completed')),
        (CANCELLED, _('Order has been cancelled and is waiting for refund')),
        (REFUNDED, _('Order has been refunded'))
    )
    status = models.CharField(_('status'), max_length=120, choices=STATUS_CHOICES)

    @hook(AFTER_CREATE)
    def create_stockrecord(self):
        for product in self.basket.products:
            # FIXME: use bulk create instead
            rec = StockRecord.objects.create(
                basket=self.basket,
                product=product,
                delta=1,
            )

    @hook(AFTER_UPDATE, when='status', has_changed=True)
    def resplenish_on_order_cancellation(self):
        # TODO: not implemented, consider using atomic transaction decorator/context manager
        # if self.status == 'refunded':
        #     ids = [stockrecord.id for stockrecord in self.basket.stockrecords]
        #     StockRecord.objects.filter(id__in=ids).delete()

        pass

