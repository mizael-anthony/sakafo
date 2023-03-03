from django.utils.translation import gettext_lazy as _
from django import forms
from flottes.models import Flotte, AllocationFlotte, DetailFlotte

class DetailFlotteForm(forms.ModelForm):

    class Meta:
        model = DetailFlotte

        fields = ('type', 'quantite',)

        labels = {
            'type': _("Type de véhicule"),
            'quantite': _("Quantité"),
        }

class AllocationFlotteForm(forms.ModelForm):

    class Meta:
        model = AllocationFlotte

        fields = ('vehicule',)

        labels = {
            'vehicule': _("Véhicule")
        }