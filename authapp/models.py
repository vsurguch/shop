from django.db import models
from django.contrib.auth.models import AbstractUser
from basketapp.models import OrderedItem
from django.utils.timezone import now
from datetime import timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save

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


class MyUserProfile(models.Model):
    user = models.OneToOneField(MyUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    city = models.CharField(max_length=32, blank=True, default='')
    photo_link = models.CharField(max_length=256, blank=True)

    @receiver(post_save, sender=MyUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            MyUserProfile.objects.create(user=instance)


    @receiver(post_save, sender=MyUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.myuserprofile.save()





