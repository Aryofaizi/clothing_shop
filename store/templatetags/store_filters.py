from django import template
register = template.Library()

@register.filter
def first_image(value):
    return value[1].image.url