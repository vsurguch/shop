
from django import forms
from django.db.models import F
from mainapp.models import Category, Author, Item

class CategoryEditForm(forms.ModelForm):
    name = forms.CharField(label='Название',
                           help_text='Например, ...',
                           widget=forms.TextInput(attrs={'class': 'edit-input'}))
    desc = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'edit-text'}))
    discount = forms.IntegerField(label='Скидка', required=False, min_value=0, max_value=100)

    class Meta:
        model = Category
        fields = '__all__'

    def clean_discount(self):
        data = self.cleaned_data['discount']
        if data:
            print('updating discount')
            self.instance.item_set.update(discount=data)
            self.instance.item_set.update(price=F('price') * (1 - data/100))
        return data


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




