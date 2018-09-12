from django.db import models
from django.contrib.auth.models import AbstractUser
from basketapp.models import OrderedItem
from django.utils.timezone import now
from datetime import timedelta

# Create your models here.

class MyUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.SmallIntegerField(blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def _get_quantity_in_basket(self):
        ordered = OrderedItem.objects.filter(user=self.id)
        if len(ordered) > 0:
            result = ordered[0].total_quantity
        else:
            result = None
        return result

    quantity_in_basket = property(_get_quantity_in_basket)

    def act_key_expired(self):
        if now() < self.activation_key_expires:
            return False
        else:
            return True




