import datetime

from django import forms
from django.utils.translation import ugettext_lazy


class DateSelectionForm(forms.Form):
    year = forms.ChoiceField(label=ugettext_lazy('Year'))
    quarter = forms.ChoiceField(label=ugettext_lazy('Quarter'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = datetime.datetime.now()
        years = [now.year - i for i in range(5)]
        quarters = [0, 1, 2, 3]
        quarters_labels = [1, 2, 3, 4]
        self.fields['year'].choices = [(year, year) for year in years]
        self.fields['quarter'].choices = zip(quarters, quarters_labels)
