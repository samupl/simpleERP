from django.contrib import admin

from apps.contacts.models import Company, Contact


class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'company_nip', 'company_regon',
                     'address_street', 'address_postcode', 'address_city', 'address_country']
    list_display = ['pk',
                    'company_name', 'company_nip', 'company_regon',
                    'address_street', 'address_postcode', 'address_city', 'address_country']


class ContactAdmin(admin.ModelAdmin):
    list_filter = ['contact_type']
    search_fields = ['company_name', 'company_nip', 'company_regon',
                     'person_first_name', 'person_last_name',
                     'address_street', 'address_postcode', 'address_city', 'address_country']
    list_display = ['pk', 'contact_type',
                    'company_name', 'company_nip', 'company_regon',
                    'person_first_name', 'person_last_name',
                    'address_street', 'address_postcode', 'address_city', 'address_country']

admin.site.register(Company, CompanyAdmin)
admin.site.register(Contact, ContactAdmin)
