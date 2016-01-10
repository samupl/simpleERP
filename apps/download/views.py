import os

from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils.encoding import smart_str


def download(request, file_name):
    full_file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    try:
        with open(full_file_path, 'rb') as fd:
            response = HttpResponse(content=fd.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(smart_str(file_name))
            return response
    except IOError:
        raise Http404
