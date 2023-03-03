import geocoder, datetime, pytz

from django.db import models
from actors.models import Client
from django.conf import settings
from parc.models import vehicule

token = 'pk.eyJ1IjoiZmFraHIiLCJhIjoiY2pseXc0djE0MHBibzN2b2h4MzVoZjk4aSJ9.ImbyLtfsfSsR_yyBluR8yQ'

class Address(models.Model):
    address = models.TextField()
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    depart = models.TimeField(blank=True, null=True)
    arrivee = models.TimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address,key=token)
        coord = g.latlng
        self.lat = coord[0]
        self.long = coord[1]
        return super(Address, self).save(*args, **kwargs)
    def __str__(self):
        return "{}".format(self.address)

class Tarif(models.Model):
    km_cost = models.FloatField(default = 15.0)
    daily_cost = models.FloatField(default = 300.0)
    hybrid_coef = models.FloatField(default = 1.0)
    electric_coef = models.FloatField(default = 1.05)
    shared_coef = models.FloatField(default = 1.10)
    velo_coef = models.FloatField(default = 0.10)
    trottinette_coef = models.FloatField(default = 0.15)
    depot_cost = models.FloatField(default = 15.0)
    livraison_coef = models.FloatField(default = 1.0)

    def __str__(self):
        return "Tarif {}".format(self.id)

class Ligne_reguliere(models.Model):
    adresse_depart = models.ForeignKey(Address,related_name="Start_address", on_delete=models.PROTECT)
    adresse_arrivee = models.ForeignKey(Address,related_name="End_address", on_delete=models.PROTECT)

    def __str__(self):
        return "Ligne entre {} et {}".format(self.adresse_depart, self.adresse_arrivee)

class voiture_reguliere(vehicule):
    ligne = models.ForeignKey(Ligne_reguliere, on_delete=models.PROTECT)

    

class voiture_demande(vehicule):

    disponible= models.BooleanField(default=True)


class Reservation(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
		related_name='%(class)s_requests_created')
    adresse_depart = models.TextField()
    adresse_arrivee = models.TextField()
    charge = models.TextField(blank=True,null=True)
    prix = models.FloatField()
    nb_passager = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        tz_France = pytz.timezone('Europe/Paris')
        d_aware = self.date_created.astimezone(tz_France)
        return "{} {}".format(self.client, d_aware.strftime("%d/%m/%Y - %H:%M:%S"))

class Reservation_Demande(Reservation):
    
    choix_type = (
		(0, 'Electric'), 
		(1, 'Hybrid'),
		(2, 'Shared'),
	)
    
    choix_statut = (
		(0, 'Impayée'), 
		(1, 'A réaliser'),
		(2, 'Annulée'),
		(3, 'Réalisée'),
	)
    
    date = models.DateField(default=datetime.date.today)
    depart = models.TimeField(blank=True, null=True)
    type = models.IntegerField(choices=choix_type)
    statut = models.IntegerField(choices=choix_statut, default=0)
    aller_retour = models.BooleanField(default=False)
    voiture = models.ForeignKey(voiture_demande, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        tz_France = pytz.timezone('Europe/Paris')
        d_aware = self.date_created.astimezone(tz_France)
        return "{} {} [{}]".format(self.client, d_aware.strftime("%d/%m/%Y - %H:%M:%S"),self.get_statut_display())

    

