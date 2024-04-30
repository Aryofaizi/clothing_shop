from django import template
from store.models import Comment
from django.core.paginator import Paginator
register = template.Library()

@register.filter
def first_image(value):
    """Gets onely the first image for the products that have multiple images."""
    return value[0].image.url

@register.filter
def last_four(value):
    """Represents the last four products created in database."""
    return value.order_by("-id")[:4]

@register.filter
def persian_number(value):
    value = str(value)
    persian_to_english = value.maketrans("1234567890", "۱۲۳۴۵۶۷۸۹۰")
    return value.translate(persian_to_english)


@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=3, on_ends=2):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number, 
                                           on_each_side=on_each_side,
                                           on_ends=on_ends)