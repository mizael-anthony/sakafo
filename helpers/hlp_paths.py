from django.conf import settings # authetification user model
from django.contrib.auth.models import User
from uuid import uuid4
import os

class PathsHelpers():
	USER_AVATAR_FOLDER = 'user_avatar_folder/' # Répertoire des avatars (photos) des utilisateurs

	def path_and_rename(instance, filename, upload_to):
		"""
		Méthode utiliséé pour remplacer automatiquement le nom de fichier par l'ID encours
		"""
		ext = filename.split('.')[-1]
		# Obtenir le nom du fichie
		if isinstance(instance, User):
			if instance.username:
				filename = '{}.{}'.format(instance.username, ext)
			else:
				# Définir le nom du fichier comme chaîne aléatoire
				filename = '{}.{}'.format(uuid4().hex, ext)
		else:
			if instance.pk:
				filename = '{}.{}'.format(instance.username, ext)
		
		# Renvoyer l'intégralité du chemin vers le fichier
		return os.path.join(upload_to, filename)