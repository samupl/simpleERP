from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ContactsAppConfig(AppConfig):
    name = 'apps.contacts'
    verbose_name = _('Contacts')

