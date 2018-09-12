from django.core.management.base import BaseCommand
from mainapp.models import Category, Item, Author
from authapp.models import MyUser
from django.contrib.auth.models import User

import json, os

JSON_PATH = 'mainapp/json'

def loadFromJSON(file_name):
    with open(os.path.join(JSON_PATH, file_name+'.json'), 'r') as f:
        return json.load(f)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = loadFromJSON('data')
        Category.objects.all().delete()
        Author.objects.all().delete()
        Item.objects.all().delete()
        for rec in data:
            if rec['model'] == 'mainapp.category':
                new_category = Category(**rec['fields'])
                new_category.save()

            if rec['model'] == 'mainapp.author':
                new_author = Author(**rec['fields'])
                new_author.save()

        for rec in data:
            if rec['model'] == 'mainapp.item':
                category_id = rec['fields']['category']
                author_id = rec['fields']['author']
                _category = Category.objects.all()[0]
                _author = Author.objects.all()[0]
                rec['fields']['category'] = _category
                rec['fields']['author'] = _author
                new_item = Item(**rec['fields'])
                new_item.save()

        # print(data)

        # # categories = loadFromJSON('categoies')
        #
        # for category in categories:
        #     new_category = Category(**category)
        #     new_category.save()
        #
        # # authors = loadFromJSON('autors')
        # Author.objects.all().delete()
        # for author in authors:
        #     new_author = Author(**author)
        #     new_author.save()
        # # items = loadFromJSON('items')
        # Item.objects.all().delete()
        # for item in items:
        #     category_name = item['category']
        #     author_name = item['author']
        #     _category = Category.objects.get(name=category_name)
        #     _author = Author.objects.get(name=author_name)
        #     item['category'] = _category
        #     item['author'] = _author
        #     new_item = Item(**item)
        #     new_item.save()
        #
        # MyUser.objects.all().delete()
        # super_user = MyUser.objects.create_superuser('admin', '', '123', age=20)
