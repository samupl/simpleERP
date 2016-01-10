import os
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def fs_static(filename, demo=True):
    if settings.DEBUG and not demo:
        static_dir = 'media'
    else:
        static_dir = 'static'
    if demo:
        ret = '/' + os.path.join(static_dir, filename)
    else:
        ret = 'file://' + os.path.join(settings.BASE_DIR, static_dir, filename)

    return ret
