from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import OrderedItem
from mainapp.models import Item
# Create your views here.

@login_required
def basket(request):
    if request.user.is_authenticated:
        all_ordered = OrderedItem.objects.filter(user=request.user)
    else:
        all_ordered = None
    context = {
        'all_ordered': all_ordered
    }
    return render(request, 'basketapp/basket.html', context)

def basket_add(request, id):
    item = Item.objects.get(id=id)
    all_ordered = OrderedItem.objects.filter(user=request.user)
    ordered = all_ordered.filter(item=item)

    if len(ordered) == 0:
        ordered_item = OrderedItem(user=request.user, item=item, quantity=1)
        ordered_item.save()
    else:
        ordered_item = ordered[0]
        ordered_item.quantity += 1
        ordered_item.save()

    context = {
        'body_class': 'basket',
        'ordered_item': ordered_item,
        'all_ordered': all_ordered
    }
    return render(request, 'basketapp/basket.html', context)


def basket_add1(request, id):
    item = Item.objects.get(id=id)
    all_ordered = OrderedItem.objects.filter(user=request.user)
    ordered = all_ordered.filter(item=item)

    if len(ordered) == 0:
        ordered_item = OrderedItem(user=request.user, item=item, quantity=1)
        ordered_item.save()
    else:
        ordered_item = ordered[0]
        ordered_item.quantity += 1
        ordered_item.save()

    # count = OrderedItem.objects.filter(user=request.user).count()
    count = all_ordered[0].total_quantity
    context = {
        'count': count,
    }
    result = render_to_string('mainapp/basket_menu.html', context)
    return JsonResponse({'result': result})


def basket_edit(request, id, quantity):
    if request.is_ajax():
        odered_item = OrderedItem.objects.get(id=int(id))
        quantity = int(quantity)

        if quantity > 0:
            odered_item.quantity = quantity
            odered_item.save()
        else:
            odered_item.delete()

        all_ordered = OrderedItem.objects.filter(user=request.user)
        context = {
            'all_ordered': all_ordered
        }
        result = render_to_string('basketapp/inc_basket_list.html', context)
        return JsonResponse({'result': result})


def basket_remove(request, id):
    if request.is_ajax():
        odered_item = OrderedItem.objects.get(id=int(id))
        odered_item.delete()

        all_ordered = OrderedItem.objects.filter(user=request.user)
        context = {
            'all_ordered': all_ordered
        }

        result = render_to_string('basketapp/inc_basket_list.html', context)

        return JsonResponse({'result': result})


def basket_menu_update(request):
    if request.user.is_authenticated:
        odered = OrderedItem.objects.filter(user=request.user)
        if len(odered) > 0:
            count = odered[0].total_quantity
        else:
            count = None
    else:
        count = None

    context = {
        'count': count
    }

    return render(request, 'mainapp/basket_menu.html', context)





