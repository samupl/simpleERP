from django.conf.urls import url
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy

from apps.costs.admin_views import costs


class DummyModel(models.Model):

    class Meta:
        verbose_name = ugettext_lazy('Costs')
        verbose_name_plural = ugettext_lazy('Costs')
        app_label = 'costs'


class DummyModelAdmin(admin.ModelAdmin):
    model = DummyModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            url(r'costs/$', costs, name=view_name),
            url(r'costs/(\d+)/(\d+)', costs, name=view_name),
        ]


admin.site.register(DummyModel, DummyModelAdmin)
