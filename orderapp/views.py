from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

# Create your views here.

from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.http import JsonResponse

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

from basketapp.models import OrderedItem
from orderapp.models import Order, OrderItem
from orderapp.forms import OrderItemForm
from mainapp.models import Item


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        order = Order.objects.filter(user=self.request.user)
        return order

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(OrderList, self).get_context_data(**kwargs)
        data['app'] = ':orders'
        return data


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orderapp:order_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = OrderedItem.objects.filter(user=self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for i, form in enumerate(formset.forms):
                    form.initial['item'] = basket_items[i].item
                    form.initial['quantity'] = basket_items[i].quantity
                    form.initial['price'] = basket_items[i].item.price
                basket_items.delete()
            else:
                formset = OrderFormSet()
        data['orderitems'] = formset
        data['app'] = ':orders'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            # if self.object.get_total_cost() == 0:
            #     self.object.delete()

            return super(OrderItemsCreate, self).form_valid(form)


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orderapp:order_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            print(self.object)
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.item.price
            data['orderitems'] = formset

        data['app'] = ':orders'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # if self.object.get_total_cost() == 0:
        #     self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orderapp:order_list')

    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     self.object.delete()
    #     return HttpResponseRedirect(self.get_success_url())


class OrderDetailView(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        # print(self.get_object().orderitems.select_related())
        context['app'] = ':orders'
        return context


def back_to_basket(request, pk):

    order = Order.objects.get(pk=pk)
    user = request.user
    for obj in order.orderitems.select_related():
        basket_item = OrderedItem(user=user, item=obj.item, quantity=obj.quantity)
        basket_item.save()
    order.delete()
    return HttpResponseRedirect(reverse('basket:basket_index'))


def get_itemprice(request, pk):
    if request.is_ajax:
        item = Item.objects.filter(pk=int(pk)).first()
        if item:
            return JsonResponse({'price': item.price})
        else:
            return JsonResponse({'price': 0})


# @receiver(pre_save, sender=OrderItem)
# def update_quantity(sender, update_fields, instance, **kwargs):
#     print(update_fields)
#     if 'quantity' in update_fields:
#         print('save')
#         instance.item.quantity -= instance.quantity
#         instance.item.save()






