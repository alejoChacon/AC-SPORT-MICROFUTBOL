from django import template
register = template.Library()

@register.filter
def resta(value,arg):
    return value - arg