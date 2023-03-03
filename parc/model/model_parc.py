from django.db import models
from helpers.hlp_paths import PathsHelpers
from actors.models import Chauffeur

def path_photo_user(instance, filename):
	"""
	Desc: Répertoire d'avatar (photo) de l'utilisateur
	"""
	return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.USER_AVATAR_FOLDER)

class vehicule(models.Model):

    choix_type = (
		(0, 'Electric'), 
		(1, 'Hybrid'),
		(2, 'Diesel'),
		(3, 'Non motorized'),
	)
    numero = models.CharField(max_length=16)
    marque = models.CharField(max_length=20)
    modele = models.CharField(max_length=20)
    nb_place = models.IntegerField(default=1)

    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.PROTECT, blank=True, null=True)

    type = models.IntegerField(choices=choix_type, default=0)
    avatar = models.ImageField(upload_to=path_photo_user, max_length=255, null=True, blank=True)

    def __str__(self):
        return "{} - {} ({})".format(self.marque, self.modele, self.numero)

