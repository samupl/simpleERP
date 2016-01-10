from django.conf.urls import include, url
from django.contrib import admin

from simpleERP.admin import configure_admin_site

import apps.invoices.urls
import apps.download.urls

configure_admin_site(admin.site)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^invoices/', include(apps.invoices.urls, namespace='invoices')),
    url(r'^download/', include(apps.download.urls, namespace='download')),
]
