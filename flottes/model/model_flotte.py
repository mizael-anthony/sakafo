from django.db import models
from django.conf import settings
from parc.models import vehicule
from django.core.validators import MinValueValidator
from decimal import Decimal
import datetime
import pytz


class Flotte(models.Model):
    choix_statut = (
		(0, 'Impayée'), 
		(1, 'A réaliser'),
		(2, 'Annulée'),
		(3, 'Réalisée'),
	)
    choix_mode_paiement = (
        (0, 'Carte bancaire'),
        (1, 'Virement'),
    )
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
		related_name='%(class)s_requests_created')
    debut = models.DateField(default=datetime.date.today)
    fin = models.DateField(default=datetime.date.today)
    charge = models.TextField(blank=True,null=True)
    prix = models.FloatField(default=0.0)
    date_created = models.DateTimeField(auto_now_add=True)
    statut = models.IntegerField(choices=choix_statut, default=0)
    mode_paiement = models.IntegerField(choices=choix_mode_paiement, default=0)

    def __str__(self):
        tz_France = pytz.timezone('Europe/Paris')
        d_aware = self.date_created.astimezone(tz_France)
        return "{} {} [{}]".format(self.client, d_aware.strftime("%d/%m/%Y - %H:%M:%S"),self.get_statut_display())

    @property
    def get_total(self):
        total = 0.0
        for o in DetailFlotte.objects.filter(flotte=self):
            total += o.prix
        return round(total, 2)
    
    @property
    def get_qte_total(self):
        total = 0
        for o in DetailFlotte.objects.filter(flotte=self):
            total += o.quantite
        return total

class vehicule_flotte(vehicule):

    disponible= models.BooleanField(default=True)

class DetailFlotte(models.Model):
    choix_type = (
		(0, 'Electric'), 
		(1, 'Hybrid'),
		(2, 'Shared'),
		(3, 'Vélo'),
		(4, 'Trottinette'),
	)
    flotte = models.ForeignKey(Flotte, on_delete=models.PROTECT)
    type = models.IntegerField(choices=choix_type)
    quantite = models.IntegerField(validators=[MinValueValidator(1)])
    prix = models.FloatField(default=0.0)

    def __str__(self):
        tz_France = pytz.timezone('Europe/Paris')
        d_aware = self.flotte.date_created.astimezone(tz_France)
        return "{} ({}) - {} {}".format(self.get_type_display(),self.quantite,self.flotte.client, d_aware.strftime("%d/%m/%Y - %H:%M:%S"))

class AllocationFlotte(models.Model):
    flotte = models.ForeignKey(Flotte, on_delete=models.PROTECT)
    vehicule = models.ForeignKey(vehicule_flotte, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        tz_France = pytz.timezone('Europe/Paris')
        d_aware = self.flotte.date_created.astimezone(tz_France)
        return "{} ({}) - {} {}".format(self.vehicule.get_type_display(),self.vehicule,self.flotte.client, d_aware.strftime("%d/%m/%Y - %H:%M:%S"))
