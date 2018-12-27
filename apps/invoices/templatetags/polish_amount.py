import slownie
from django import template

register = template.Library()


@register.simple_tag
def polish_amount(amount, fulls_unit, halves_unit):
    string = str(amount)
    fulls, halves = string.split('.')
    fulls = slownie.slownie(fulls, unit=fulls_unit)
    halves = slownie.slownie(halves, unit=halves_unit)
    return '{}, {}'.format(fulls, halves)
