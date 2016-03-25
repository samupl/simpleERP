from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext_lazy
from django_countries import countries
from django_countries.fields import CountryField

COUNTRIES = [(ugettext_lazy(name), code) for (name, code) in list(countries)]


class Company(models.Model):
    # Company credentials
    company_name = models.CharField(_('Company name'), max_length=1024, null=True, blank=True)
    company_nip = models.CharField(_('NIP'), max_length=10, null=True, blank=True)
    company_regon = models.CharField(_('REGON'), max_length=9, null=True, blank=True)

    # Common address credentials
    address_city = models.CharField(_('City'), max_length=1024, null=True, blank=True)
    address_street = models.CharField(_('Street'), max_length=1024, null=True, blank=True)
    address_postcode = models.CharField(_('Postal code'), max_length=10, null=True, blank=True)
    # address_country = models.CharField(_('Country'), max_length=512, null=True, blank=True, choices=COUNTRIES)
    address_country = CountryField(max_length=512, null=True, blank=True)

    # Bank number
    bank_account_number = models.CharField(_('Bank account number'), max_length=512, null=True, blank=True)

    @property
    def company(self):
        return '{company} (NIP: {nip}, REGON: {regon})'.format(
            company=self.company_name,
            nip=self.company_nip,
            regon=self.company_regon
        )

    @property
    def address_country_verbose(self):
        return countries.countries[self.address_country]

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')


class Contact(models.Model):
    TYPE_PERSONAL = 1
    TYPE_COMPANY = 2

    TYPES = {
        TYPE_PERSONAL: _('Private person'),
        TYPE_COMPANY: _('Company')
    }

    contact_type = models.PositiveIntegerField(_('Type'), choices=list(TYPES.items()))

    # Private person credentials
    person_first_name = models.CharField(_('First name'), max_length=256, null=True, blank=True)
    person_last_name = models.CharField(_('Last name'), max_length=256, null=True, blank=True)

    # Company credentials
    company_name = models.CharField(_('Company name'), max_length=1024, null=True, blank=True)
    company_nip = models.CharField(_('NIP'), max_length=10, null=True, blank=True)
    company_regon = models.CharField(_('REGON'), max_length=9, null=True, blank=True)

    # Common address credentials
    address_city = models.CharField(_('City'), max_length=1024, null=True, blank=True)
    address_street = models.CharField(_('Street'), max_length=1024, null=True, blank=True)
    address_postcode = models.CharField(_('Postal code'), max_length=10, null=True, blank=True)
    address_country = models.CharField(_('Country'), max_length=512, null=True, blank=True, choices=COUNTRIES)

    @property
    def address(self):
        return '{street}, {postcode} {city}, {country}'.format(
                street=self.address_street,
                postcode=self.address_postcode,
                city=self.address_city,
                country=self.address_country)

    @property
    def name(self):
        return '{first_name} {last_name}'.format(
                first_name=self.person_first_name,
                last_name=self.person_last_name)

    @property
    def company(self):
        return '{company} (NIP: {nip}, REGON: {regon})'.format(
            company=self.company_name,
            nip=self.company_nip,
            regon=self.company_regon
        )

    @property
    def address_country_verbose(self):
        return countries.countries[self.address_country]

    @property
    def is_company(self):
        return self.contact_type == self.TYPE_COMPANY

    def __str__(self):
        if self.contact_type == self.TYPE_COMPANY:
            credentials = self.company
        else:
            credentials = self.name

        return '{type}: {credentials}'.format(
            type=self.TYPES.get(self.contact_type),
            credentials=credentials
        )

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
