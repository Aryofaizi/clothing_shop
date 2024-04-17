from django import template
from store.models import Comment
register = template.Library()

@register.filter
def first_image(value):
    """Gets onely the first image for the products that have multiple images."""
    return value[1].image.url

@register.filter
def last_four(value):
    """Represents the last four products created in database."""
    return value.order_by("-id")[:4]

@register.filter
def persian_number(value):
    value = str(value)
    persian_to_english = value.maketrans("1234567890", "۱۲۳۴۵۶۷۸۹۰")
    return value.translate(persian_to_english)