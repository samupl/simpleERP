from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^issue/(\d+)$', views.issue, name='issue'),
    url(r'^render/(\d+)$', views.render_invoice, name='render_invoice'),
    url(r'^render/(\d+)/pdf$', views.render_invoice_pdf, name='render_invoice_pdf')
]
