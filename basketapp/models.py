from django.db import models
from django.utils.functional import cached_property
from mainapp.models import Item
from shop import settings

# Create your models here.
class BasketQuerySet(models.QuerySet):
    def delete(self):
        for object in self:
            object.item.quantity += object.quantity
            object.item.save()
        super(BasketQuerySet, self).delete()


class OrderedItem(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(verbose_name='quantity', default=0)
    add_datetime = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    @cached_property
    def get_items_cached(self):
        all_ordered = OrderedItem.objects.filter(user=self.user)
        return all_ordered

    def _get_total_quantity(self):
        all_ordered = self.get_items_cached
        result = sum(map(lambda x: x.quantity, all_ordered))
        return result

    total_quantity = property(_get_total_quantity)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.item.quantity -= self.quantity
        self.item.save()
        super(OrderedItem, self).save()

    def delete(self, using=None, keep_parents=False):
        self.item.quantity += self.quantity
        self.item.save()
        super(OrderedItem, self).delete()


