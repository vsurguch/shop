from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import MyUser

# Create your views here.

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

    context = {'title': title, 'body_class': 'authform', 'login_form': login_form, 'next': next }
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
                print('Сообщение отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('Ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))

            # return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = UserRegisterForm().as_p()

    context = {'title': title, 'body_class': 'authform', 'register_form': register_form}
    return render(request, 'authapp/register.html', context)

def edit(request):
    title = 'edit'

    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('main:index'))

    else:
        edit_form = UserEditForm(instance=request.user)

    context = {'title': title, 'body_class': 'authform',  'edit_form': edit_form}
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








