from django.utils.translation import ugettext_lazy as _


def configure_admin_site(admin_site):
    # Text to put at the end of each page's <title>.
    admin_site.site_title = _('SimpleERP Admin site')

    # Text to put in each page's <h1>.
    admin_site.site_header = _('SimpleERP Administration')

    # Text to put at the top of the admin index page.
    admin_site.index_title = _('SimpleERP administration')
