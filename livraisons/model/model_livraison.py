import datetime, pytz

from django.db import models
from django.conf import settings

from django.core.validators import MaxValueValidator, MinValueValidator

from reservation.models import voiture_demande,Reservation
token = 'pk.eyJ1IjoiZmFraHIiLCJhIjoiY2pseXc0djE0MHBibzN2b2h4MzVoZjk4aSJ9.ImbyLtfsfSsR_yyBluR8yQ'


class Livraison(Reservation):
    
    choix_statut = (
		(0, 'Impayée'), 
		(1, 'A réaliser'),
		(2, 'Annulée'),
		(3, 'Réalisée'),
	)
    
    date = models.DateField(default=datetime.date.today)
    depart = models.TimeField(blank=True, null=True)
    statut = models.IntegerField(choices=choix_statut, default=0)
    aller_retour = models.BooleanField(default=False)
    colis_1 = models.BooleanField(default=False)
    weight_1 = models.FloatField(default=0.0, validators=[MaxValueValidator(25.0), MinValueValidator(0.0)])
    colis_2 = models.BooleanField(default=False)
    weight_2 = models.FloatField(default=0.0, validators=[MaxValueValidator(25.0), MinValueValidator(0.0)])
    colis_3 = models.BooleanField(default=False)
    weight_3 = models.FloatField(default=0.0, validators=[MaxValueValidator(25.0), MinValueValidator(0.0)])
    colis_4 = models.BooleanField(default=False)
    weight_4 = models.FloatField(default=0.0, validators=[MaxValueValidator(25.0), MinValueValidator(0.0)])
    voiture = models.ForeignKey(voiture_demande, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        tz_France = pytz.timezone('Europe/Paris')
        d_aware = self.date_created.astimezone(tz_France)
        return "{} {} [{}]".format(self.client, d_aware.strftime("%d/%m/%Y - %H:%M:%S"),self.get_statut_display())