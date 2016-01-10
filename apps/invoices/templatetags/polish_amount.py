import slownie
from django import template

register = template.Library()


@register.simple_tag
def polish_amount(amount):
    string = str(amount)
    fulls, halves = string.split('.')
    fulls = slownie.slownie(fulls, unit=slownie.UNIT_ZLOTY)
    halves = slownie.slownie(halves, unit=slownie.UNIT_GROSZ)
    return '{}, {}'.format(fulls, halves)
