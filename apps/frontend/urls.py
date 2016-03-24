from django.conf.urls import url
from .views import index, view_provider


urlpatterns = [
    url(r'^views/(.*)', view_provider, name='view_provider'),
    url(r'^', index, name='index')
]
