from django.test import TestCase
from django.test.client import Client
from mainapp.models import Category, Item, Author
from django.core.management import call_command

# Create your tests here.

# пришлось исключить из базы все нижеперечисленное, иначе InegrityError
# python manage.py dumpdata -e=contenttypes -e=sessions -e=auth -e=admin -o test_db.json

class TestMainappSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

        for item in Item.objects.all():
            response = self.client.get(f'/item/{item.id}')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'orderapp', 'basketapp')

