
from django import forms
from mainapp.models import Category, Author, Item

class CategoryEditForm(forms.ModelForm):
    name = forms.CharField(label='Название',
                           help_text='Например, ...',
                           widget=forms.TextInput(attrs={'class': 'edit-input'}))
    desc = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'edit-text'}))

    class Meta:
        model = Category
        fields = '__all__'


class AuthorEditForm(forms.ModelForm):
    name = forms.CharField(label='Имя Автора',
                           help_text='Например, Клод Моне...',
                           widget=forms.TextInput(attrs={'class': 'edit-input'}))

    class Meta:
        model = Author
        fields = '__all__'


class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'




