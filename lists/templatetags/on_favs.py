from django import template
from lists import models as lists_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    the_list = lists_models.List.objects.get_or_none(user=user, name="Избранное")
    return room in the_list.rooms.all()