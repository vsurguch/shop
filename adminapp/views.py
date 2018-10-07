from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection

from mainapp.models import Category, Author, Item
from .forms import CategoryEditForm, AuthorEditForm, ItemEditForm

# Create your views here.

def main(request):
    context = {
        'text': 'hello',
    }
    return render(request, 'adminapp/main.html', context)

def get_all_objects(T):
    objects_list = T.objects.all()
    return objects_list

@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    categories_list = Category.objects.all()

    context = {
        'title': 'Categories',
        'to_add': 'категорию',
        'link_create': 'admin:create_category',
        'link_edit': 'admin:edit_category',
        'link_delete': 'admin:delete_category',
        'objects_list': categories_list
    }

    return render(request, 'adminapp/list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def authors(request):
    authors_list = Author.objects.all()

    context = {
        'title': 'Authors',
        'to_add': 'автора',
        'link_create': 'admin:create_author',
        'link_edit': 'admin:edit_author',
        'link_delete': 'admin:delete_author',
        'objects_list': authors_list
    }

    return render(request, 'adminapp/list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def items(request):
    items_list = Item.objects.all()

    context = {
        'title': 'Items',
        'to_add': 'товар',
        'link_create': 'admin:create_item',
        'link_edit': 'admin:edit_item',
        'link_delete': 'admin:delete_item',
        'objects_list': items_list
    }

    return render(request, 'adminapp/list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def create_category(request):
    if request.method == 'POST':
        form = CategoryEditForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        form = CategoryEditForm()
        context = {
            'title': 'Create Category',
            'form': form,
        }

    return render(request, 'adminapp/edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def create_author(request):
    if request.method == 'POST':
        form = AuthorEditForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:authors'))
    else:
        form = AuthorEditForm()
        context = {
            'title': 'Create Author',
            'form': form,
        }

    return render(request, 'adminapp/edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def create_item(request):
    if request.method == 'POST':
        form = ItemEditForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:items'))
    else:
        form = ItemEditForm()
        context = {
            'title': 'Create Item',
            'form': form,
        }

    return render(request, 'adminapp/edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def edit_category(request, id):
    category = get_object_or_404(Category, id=int(id))
    if request.method == 'POST':
        form = CategoryEditForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        form = CategoryEditForm(instance=category)
        context = {
            'title': 'Edit Category',
            'form': form,
        }

    return render(request, 'adminapp/edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def edit_author(request, id):
    author = get_object_or_404(Author, id=int(id))
    if request.method == 'POST':
        form = AuthorEditForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:authors'))
    else:
        form = AuthorEditForm(instance=author)
        context = {
            'title': 'Edit Author',
            'form': form,
        }

    return render(request, 'adminapp/edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def edit_item(request, id):
    item = get_object_or_404(Item, id=int(id))
    if request.method == 'POST':
        form = ItemEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:items'))
    else:
        form = ItemEditForm(instance=item)
        context = {
            'title': 'Edit Item',
            'form': form,
        }

    return render(request, 'adminapp/edit.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_category(request):
    if request.method == 'POST':
        if 'id' in request.POST:
            category = get_object_or_404(Category, id=request.POST['id'])
            category.delete()
    return HttpResponseRedirect(reverse('admin:categories'))


@user_passes_test(lambda u: u.is_superuser)
def delete_author(request):
    if request.method == 'POST':
        if 'id' in request.POST:
            author = get_object_or_404(Author, id=request.POST['id'])
            author.delete()
    return HttpResponseRedirect(reverse('admin:authors'))


@user_passes_test(lambda u: u.is_superuser)
def delete_item(request):
    if request.method == 'POST':
        if 'id' in request.POST:
            item = get_object_or_404(Item, id=request.POST['id'])
            item.delete()
    return HttpResponseRedirect(reverse('admin:items'))


def db_profile_by_type(prefix, query_type, queries):
    update_queries = list(filter(lambda x: query_type in x['sql'], queries))
    print(f'db_profile {query_type} for {prefix}')
    [print(query['sql']) for query in update_queries]

@receiver(pre_save, sender=Category)
def update_items_for_category(sender, instance, **kwargs):
    print('updating ...')
    if instance.pk:
        # discount = instance.discount
        # instance.item_set.update(discount=discount)

        if instance.is_active:
            instance.item_set.update(is_active=True)
        else:
            instance.item_set.update(is_active=False)
    db_profile_by_type(sender, 'UPDATE', connection.queries)


