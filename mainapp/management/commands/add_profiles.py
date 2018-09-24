
from django.core.management.base import BaseCommand
from authapp.models import MyUser, MyUserProfile

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = MyUser.objects.all()
        for user in users:
            user_profile = MyUserProfile.objects.create(user=user)
            user_profile.save()