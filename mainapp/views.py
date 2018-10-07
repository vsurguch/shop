from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.db.models import Q

from .models import Category, Author, Item

# Create your views here.
def index(request):
    context = {
        'title': 'Интернет-магазин произведений искусства',
        'body_class': 'homepage',
    }
    return render(request, 'mainapp/index_.html', context)

def catalog(request):
    items = Item.objects.all()
    authors = Author.objects.all()
    categories = Category.objects.all()

    if request.method == 'GET' and len(request.GET) > 0:
        try:
            author_id = int(request.GET['authors'])
            category_id = int(request.GET['categories'])
            if author_id != 0:
                items = items.filter(author__id = author_id)
            if category_id != 0:
                items = items.filter(category__id = category_id)
        except Exception as e:
            # print(e)
            raise Http404


    context = {
        'title': 'Masterpiece. Каталог.',
        'body_class': 'catalog',
        'items': items,
        'categories': categories,
        'authors': authors
    }
    return render(request, 'mainapp/catalog_.html', context)

def catalog_update(request):
    items = Item.objects.all()

    if request.method == 'GET' and len(request.GET) > 0:
        try:
            author_id = int(request.GET['authors'])
            categories = request.GET['categories']
            categories_id = list(map(lambda x: int(x), categories.split(',')))

            if author_id != 0:
                items = items.filter(author__id=author_id)

            if categories_id[0] != 0:
                filter_options = Q(category_id=categories_id[0])
                if len(categories_id) > 1:
                    for category_id in categories_id[1:]:
                        filter_options = filter_options | Q(category_id=category_id)
                items = items.filter(filter_options)

        except Exception as e:
            # print(e)
            raise Http404

    context = {
        'items': items,
    }
    return render(request, 'mainapp/catalog_update.html', context)

def contacts(request):
    context = {
        'title': 'Masterpiece. Контакты.',
        'body_class': 'contacts',
    }
    return render(request, 'mainapp/contacts_.html', context)

def item_view(request, id):
    try:
        item = Item.objects.get(id=id)
        context = {
            'title': item.name,
            'body_class': 'item',
            'item': item
        }
    except Item.DoesNotExist:
        raise Http404("Item does not exist")
    return render(request, 'mainapp/item_detail.html', context)
