from django.utils.translation import gettext_lazy as _
from django import forms

from livraisons.models import Livraison


class LivraisonForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ('adresse_depart','adresse_arrivee','colis_1','weight_4','colis_2','colis_3','colis_4','weight_1','weight_2','weight_3', 'date','depart','prix','aller_retour')
        labels = {
            'adresse_depart': _("Adresse de départ"),
            'adresse_arrivee': _("Adresse de destination"),
            'colis_1': _("1er colis"),
            'colis_2': _("2ème colis"),
            'colis_3': _("3ème colis"),
            'colis_4': _("4ème colis"),
            'weight_1': _("Poids (kg)"),
            'weight_2': _("Poids (kg)"),
            'weight_3': _("Poids (kg)"),
            'weight_4': _("Poids (kg)"),
            'date': _("Date de prise en charge"),
            'depart': _("Heure de prise en charge"),
            'aller_retour': _("Aller-retour"),
            'prix': _("Prix (€)"),
        }
        widgets = {
          'adresse_depart': forms.Textarea(attrs={'rows':3}),
          'adresse_arrivee': forms.Textarea(attrs={'rows':3}),
        }
    
    def __init__(self, *args, **kwargs):
        _type = kwargs.pop('type', None)
        super(LivraisonForm, self).__init__(*args, **kwargs)
        self.fields['adresse_depart'].widget.attrs['readonly'] = True
        self.fields['adresse_arrivee'].widget.attrs['readonly'] = True
        self.fields['prix'].widget.attrs['readonly'] = True
    
    def clean(self):
        """ Règle appliquée au champs note """
        colis_1 = self.cleaned_data.get('colis_1')
        colis_2 = self.cleaned_data.get('colis_2')
        colis_3 = self.cleaned_data.get('colis_3')
        colis_4 = self.cleaned_data.get('colis_4')
        weight_1 = self.cleaned_data.get('weight_1')
        weight_2 = self.cleaned_data.get('weight_2')
        weight_3 = self.cleaned_data.get('weight_3')
        weight_4 = self.cleaned_data.get('weight_4')
        
        if weight_1 > 0.0 and not colis_1:
            raise forms.ValidationError(_("Le 1er colis doit être sélectionné"))
        if weight_2 > 0.0 and not colis_2:
            raise forms.ValidationError(_("Le 2ème colis doit être sélectionné"))
        if weight_3 > 0.0 and not colis_3:
            raise forms.ValidationError(_("Le 3ème colis doit être sélectionné"))
        if weight_4 > 0.0 and not colis_4:
            raise forms.ValidationError(_("Le 4ème colis doit être sélectionné"))
        