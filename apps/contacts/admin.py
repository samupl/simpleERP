from django.contrib import admin

from apps.contacts.models import Company, Contact, CompanyBankAccount


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


class CompanyBankAccountAdmin(admin.ModelAdmin):
    search_fields = ['bank_name']
    list_display = [
        'slug', 'bank_account_number', 'iban', 'bank_name', 'bank_name',
    ]


admin.site.register(Company, CompanyAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(CompanyBankAccount, CompanyBankAccountAdmin)
