from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm, UserProfileEditForm
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import MyUser
import requests

# Create your views here.
fb_app_id = 435213300218856
vk_app_id = 6693926
vk_secret = '95AoBAVeadIGXqX6SJEc'
redirect_uri = "http://localhost:8000/auth/login-vk"
fb_auth_link = f'https://www.facebook.com/v3.1/dialog/oauth?client_id={fb_app_id}&redirect_uri={redirect_uri}&state={{\"{{st=state123abc,ds=123456789}}\"}}'
vk_auth_link = f'https://oauth.vk.com/authorize?client_id={vk_app_id}&display=page&redirect_uri={redirect_uri}&scope=friends&response_type=code&v=5.85'
# vk_access_token = f'https://oauth.vk.com/access_token?client_id={vk_app_id}&client_secret={vk_secret}&redirect_uri={redirect_uri}&code={code}'


def login(request):
    title = 'Login'

    login_form = UserLoginForm(data = request.POST or None).as_p()
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('main:index'))

    context = {'title': title,
               'body_class': 'authform',
               'login_form': login_form,
               'next': next,
               'vk_link': vk_auth_link}

    if 'auth_email' in request.session:
        if request.session['auth_email'] == 'sent':
            context['msg'] = 'Вам на e-mail отправлено сообщение с кодом активации'
        elif request.session['auth_email'] == 'not sent':
            context['msg'] = 'Сообщение с кодом активации на e-mail отправить не удалось'

    return render(request, 'authapp/login.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))

def register(request):
    title = 'register'

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_email(user):
                # print('Сообщение отправлено')
                request.session['auth_email'] = 'sent'
            else:
                # print('Ошибка отправки сообщения')
                request.session['auth_email'] = 'not sent'
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = UserRegisterForm()

    context = {'title': title, 'body_class': 'authform', 'register_form': register_form}
    return render(request, 'authapp/register.html', context)

def edit(request):
    title = 'edit'

    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        edit_profile_form = UserProfileEditForm(request.POST, instance=request.user.myuserprofile)
        if edit_form.is_valid() and edit_profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('main:index'))

    else:
        edit_form = UserEditForm(instance=request.user)
        edit_profile_form = UserProfileEditForm(instance=request.user.myuserprofile)

    context = {'title': title,
               'body_class': 'authform',
               'edit_form': edit_form,
               'profile_form': edit_profile_form}
    if request.user.myuserprofile.photo_link != '':
        context['avatar_vk'] = request.user.myuserprofile.photo_link

    return render(request, 'authapp/edit.html', context)

def send_email(user):
    link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи перейдите по ссылке {settings.DOMAIN_NAME}{link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

def verify(request, email, key):
    user = get_object_or_404(MyUser, email=email)
    if user.activation_key == key:
        user.is_active = True
        user.save()
        print(f'now user {user.username} is active')
    return HttpResponseRedirect(reverse('auth:login'))

def login_vk(request):
    if 'code' in request.GET.keys():
        code = request.GET['code']
        params = {
            'client_id': vk_app_id,
            'client_secret': vk_secret,
            'redirect_uri': redirect_uri,
            'code': code
        }
        r = requests.get('https://oauth.vk.com/access_token', params=params)
        resp = r.json()
        if 'access_token' in resp:
            token = resp['access_token']
            id = resp['user_id']
            params = {
                'user_ids': id,
                'fields': 'photo_50,city,bdate',
                'access_token': token,
                'v': '5.85'
            }
            r = requests.get('https://api.vk.com/method/users.get', params=params)
            resp = r.json()
            userid = str(resp['response'][0]['id'])
            firstname = resp['response'][0]['first_name']
            lastname = resp['response'][0]['last_name']
            photo_link = resp['response'][0].get('photo_50')
            city = resp['response'][0].get('city')
            username = firstname + '_' +lastname

            users = MyUser.objects.filter(username=username)
            if len(users) == 0:
                new_user = MyUser(username=username, age=100)
                new_user.set_password('vkdefault')
                new_user.save()
                if city:
                    new_user.myuserprofile.city = city['title']
                if photo_link:
                    new_user.myuserprofile.photo_link = photo_link
                new_user.save()
            user = auth.authenticate(username=username, password='vkdefault')
            auth.login(request, user)
    else:
        print('авторизация через VK не удалась')

    return HttpResponseRedirect(reverse('main:index'))








