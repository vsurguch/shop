
from django import forms
from orderapp.models import Order, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', )


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='Price', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'item':
                field.widget.attrs['class'] = 'order_item_select'


