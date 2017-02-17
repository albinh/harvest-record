from django import template
from django.utils.safestring import mark_safe
from ..models import Customer
register = template.Library()
print("test")
@register.simple_tag
def customer_options():
    str=''
    for c in Customer.objects.all():
        str=str+'<option value="{0}">{1}</option>'.format(c.pk, c.name)
    str = mark_safe(str)
    return str