from django.db import models
from django.contrib.auth.models import User
from helpers.hlp_paths import PathsHelpers
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import datetime

def path_photo_user(instance, filename):
	"""
	Desc: Répertoire d'avatar (photo) de l'utilisateur
	"""
	return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.USER_AVATAR_FOLDER)

class Chauffeur(User):
	choix_sexe = (
		(0, 'Femme'), 
		(1, 'Homme'),
	)

	motif_sortie = (
		(0, 'Démission'), 
		(1, 'Licenciement'),
		(2, 'Retraite'),
		(3, 'Décès'),
		(4, 'Fin de contrat'),
		(5, 'Autre'),
	)
	
	matricule = models.IntegerField(unique=True,null=True)
	sexe = models.IntegerField(choices=choix_sexe, default=1)
	phone = models.CharField(max_length=16, blank=True, null=True)
	avatar = models.ImageField(upload_to=path_photo_user, max_length=255, null=True, blank=True)
	date_embauche = models.DateField(verbose_name="date d'embauche", default=datetime.date.today)
	date_demission = models.DateField(verbose_name='date demission', null=True)
	motif = models.IntegerField(choices=motif_sortie, null=True)

	class Meta:
		ordering = ['id',]
	
	def __str__(self):

		return "{} - {} {}".format(self.matricule, self.last_name, self.first_name)
	
	@property
	def full_name(self):
		return '{} {}'.format(self.first_name, self.last_name if self.first_name.upper() != self.last_name.upper() else '')

class Client(User):
	choix_sexe = (
		(0, 'Femme'), 
		(1, 'Homme'),
	)

	numero = models.IntegerField(unique=True,null=True)
	sexe = models.IntegerField(choices=choix_sexe, default=1)
	phone = models.CharField(max_length=16, blank=True, null=True)
	avatar = models.ImageField(upload_to=path_photo_user, max_length=255, null=True, blank=True)

	class Meta:
		ordering = ['id',]
	
	def __str__(self):

		return "{} {}".format(self.last_name, self.first_name)
	
	@property
	def full_name(self):
		return '{} {}'.format(self.first_name, self.last_name if self.first_name.upper() != self.last_name.upper() else '')
