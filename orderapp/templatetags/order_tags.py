from django import template
from orderapp.models import Order

register = template.Library()

def get_status(status):
    return

register.filter('get_status', get_status)