from django import template

register = template.Library()


@register.filter
def capitals(value):
    print(value)
    return value.capitalize()
