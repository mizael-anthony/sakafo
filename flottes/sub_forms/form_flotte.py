from django.utils.translation import gettext_lazy as _
from django import forms
from flottes.models import Flotte
import datetime

class FlotteForm(forms.ModelForm):

    class Meta:
        model = Flotte

        fields = ('debut','fin',)

        labels = {
            'debut': _("Début de la location"),
            'fin': _("Fin de la location")
        }
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)

        super(FlotteForm, self).__init__(*args,**kwargs)