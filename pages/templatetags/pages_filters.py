from django import template

register = template.Library()


@register.filter
def multiple_paragraph(value):
    value = value.split(" ")
    value_length = len(value) // 4
    return [" ".join(value[:value_length]),
            " ".join(value[value_length: value_length*2]),
            " ".join(value[value_length*2: value_length*3]),
            " ".join(value[value_length*3:])
            ]
    
    
@register.filter
def get_image(value, index):
    return value[index].image.url
    