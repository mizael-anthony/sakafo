from django.utils.translation import gettext_lazy as _
from django import forms

from reservation.models import Reservation_Demande


class ReservationDemandeForm(forms.ModelForm):
    class Meta:
        model = Reservation_Demande
        fields = ('adresse_depart','adresse_arrivee','nb_passager', 'date','depart','prix','type','aller_retour')
        labels = {
            'adresse_depart': _("Adresse de départ"),
            'adresse_arrivee': _("Adresse de destination"),
            'nb_passager': _("Passagers"),
            'date': _("Date de prise en charge"),
            'depart': _("Heure de prise en charge"),
            'aller_retour': _("Aller-retour"),
            'prix': _("Prix (€)"),
        }
        
    
    def __init__(self, *args, **kwargs):
        _type = kwargs.pop('type', None)
        super(ReservationDemandeForm, self).__init__(*args, **kwargs)
        self.fields['adresse_depart'].widget.attrs['readonly'] = True
        self.fields['adresse_arrivee'].widget.attrs['readonly'] = True
        self.fields['prix'].widget.attrs['readonly'] = True
        self.fields['type'].widget.attrs['readonly'] = True
        if _type:
            self.initial['type'] = int(_type) 
        # self._type = 1
        