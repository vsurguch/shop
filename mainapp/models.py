from django.db import models

# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=64, unique=True)
    desc = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'


class Author(models.Model):

    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):

    name = models.CharField(max_length=256)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    img = models.ImageField(upload_to='media', blank = True)
    short_desc = models.CharField(max_length=256, null=True)
    detailed_desc = models.TextField(blank=True)
    years = models.CharField(max_length=32, null=True)
    tech = models.CharField(max_length=64, null=True)
    width = models.SmallIntegerField(null=True)
    height = models.SmallIntegerField(null=True)
    price = models.DecimalField(max_digits=7, decimal_places=0, default=0)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.author})'




