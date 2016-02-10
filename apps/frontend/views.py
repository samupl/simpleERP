from django.http import Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist


def index(request):
    return render(request, 'frontend/index.html')


def view_provider(request, view_url):
    try:
        return render(request, 'frontend/views/' + view_url)
    except TemplateDoesNotExist:
        raise Http404
