from django.db import models
from mainapp.models import Item
from shop import settings

# Create your models here.

class OrderedItem(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(verbose_name='quantity', default=0)
    add_datetime = models.DateTimeField(auto_now_add=True)

    def _get_total_quantity(self):
        all_ordered = OrderedItem.objects.filter(user=self.user)
        result = sum(map(lambda x: x.quantity, all_ordered))
        return result

    total_quantity = property(_get_total_quantity)

