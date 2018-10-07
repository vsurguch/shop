from django.test import TestCase
from django.test.client import Client
from authapp.models import MyUser
from django.core.management import call_command
from shop import settings

# Create your tests here.

class TestAuthapp(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.superuser = MyUser.objects.create_superuser('admin2', 'admin2@test.com', '123', age=20)

        self.user = MyUser.objects.create_user('user', 'user@test.com', '123', age=20)


    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Пользователь', status_code=200)

        self.client.login(username='admin2', password='123')
        response = self.client.get('/auth/login/')
        self.assertEqual(response.context['user'], self.superuser)
        self.assertFalse(response.context['user'].is_anonymous)

    def test_user_logout(self):
        self.client.login(username='user', password='123')
        response = self.client.get('/auth/login/')
        self.assertEqual(response.context['user'], self.user)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_credentinals = {
            'username': 'user3',
            'first_name': 'User',
            'last_name': 'User',
            'password1': '123',
            'password2': '123',
            'email': 'user3@test.com',
            'age': '20',
        }

        response = self.client.post('/auth/register/', data=new_user_credentinals)
        self.assertEqual(response.status_code, 302)

        new_user = MyUser.objects.get(username=new_user_credentinals['username'])
        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_credentinals['email']}/{new_user.activation_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 302)
        new_user = MyUser.objects.get(username=new_user_credentinals['username'])
        self.assertTrue(new_user.is_active)


        self.client.login(username=new_user_credentinals['username'],
                          password=new_user_credentinals['password1'])

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, new_user_credentinals['username'])



    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'orderapp', 'basketapp')