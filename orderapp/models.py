from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from mainapp.models import Item

# Create your models here.

class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCELED = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, ''),
        (PROCEEDED, 'обрабатывается'),
        (PAID, 'оплачено'),
        (READY, 'готов'),
        (CANCELED, 'отменено')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering =('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ: {self.id}'

    @cached_property
    def get_items_cached(self):
        items = self.orderitems.select_related()
        return items

    def get_total_quantity(self):
        items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, items)))

    def get_items_category_quantity(self):
        items = self.get_items_cached
        return len(items)

    def get_total_cost(self):
        items = self.get_items_cached
        return sum(list(map(lambda x: x.get_item_cost(), items)))

    def delete(self):
        for item in self.orderitems.select_related():
            item.item.quantity += item.quantity
            item.item.save()

        super(Order, self).delete()

        # self.is_active = False
        # self.save()

class OrderItemsQuerySet(models.QuerySet):
    def delete(self):
        for obj in self:
            obj.item.quantity += obj.quantity
            obj.item.save()
        super(OrderItemsQuerySet, self).delete()


class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, verbose_name='продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    objects = OrderItemsQuerySet.as_manager()

    def get_item_cost(self):
        return self.item.price * self.quantity

    def delete(self):
        self.item.quantity += self.quantity
        self.item.save()
        super(OrderItem, self).delete()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=False):
        self.item.quantity -= self.quantity
        self.item.save()
        super(OrderItem, self).save()

