
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from authapp.models import MyUser, MyUserProfile
import random, hashlib

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = MyUser
        fields = {'username', 'password'}

    # def __init__(self, *args, **kwargs):
    #     super(UserLoginForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm):
    # username = forms.CharField(label='Username')
    # password = forms.PasswordInput()
    # password1 = forms.PasswordInput()
    # email = forms.CharField(label='E-mail')
    # age = forms.IntegerField(label='age')
    # avatar = forms.ImageField(label='avatar')

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = UserCreationForm.Meta.fields + ('email', 'age', 'avatar')

    def save(self, commit=True):
        user=super(UserRegisterForm, self).save()

        user.is_active = False

        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user

    # def __init__(self, *args, **kwargs):
    #     super(UserCreationForm, self).__init__(*args, **kwargs)
    #     self.fields['avatar'].widget.attrs['class'] = 'label_avatar'


class UserEditForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = {'first_name', 'username', 'password', 'email', 'age', 'avatar'}

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = MyUserProfile
        fields = {'city'}




