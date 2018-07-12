from urllib.parse import quote_plus
from django import template

register = template.Library()


@register.filter #v31 registro como un filtro la librería "register"
def urlify(value):
    return quote_plus(value)

