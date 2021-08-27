import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks(default 3 weeks)")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Verifier si la date entree n'est pas passé
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Verifier si la date entree est dans l'intervalle (4 semaines a compter d'aujourd'hui)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Renvoyer toujours des données Effacer
        return data