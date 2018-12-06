from django import template

register = template.Library()


@register.filter(name='_concat')
def concat(value, arg):
    return f"{value} {arg}"