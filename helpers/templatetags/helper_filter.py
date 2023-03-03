from django import template
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.safestring import mark_safe
import re

from reservation.models import Client

register = template.Library()

#------------------------------------------------------------
@register.filter()
def is_inst_client(value):
	if hasattr(value,'client'):
		return isinstance(value.client,Client)
	return False

#------------------------------------------------------------
@register.filter()
def get_invoice_date(value):
	if value:
		return value.strftime("%Y%m%d")
	return ''

#------------------------------------------------------------
@register.filter()
def get_ht(value):
	
	return round(value/1.1,1)

#------------------------------------------------------------
@register.filter()
def get_tva(value):
	
	return round(value - (value/1.1),1)

#------------------------------------------------------------
@register.filter()
def phone_format(tel):
	"""
	Convertir le numero du tel en +xxx xxxxxxx
	"""
	if tel is None or tel=='':
		return ''
	
	first = tel[0:3]
	second = tel[3:5]
	third = tel[5:8]
	forth = tel[8:10]
	res = "<span class='text-dark'><i class='fa fa-phone'><i/>&nbsp;" + first + ' ' + second + ' ' + third + ' ' + forth + "</span>"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def email_format(email):
	"""
	Convertir le numero du tel en +xxx xxxxxxx
	"""
	if email is None or email=='':
		return ''
	
	res = "<a href='mailto:" + email + "'class='text-blue' title='Envoyer un mail à cette adresse'><i class='fa fa-envelope'></i>&nbsp;" + email + "</a>"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def date_format(date):
	"""
	Convertir date en string
	"""
	if date is None or date=="":
		return ''
	
	res = "<span class='badge badge-info'>" + date.strftime("%d/%m/%Y") + "</span>"

	return mark_safe(res)


#------------------------------------------------------------
@register.filter()
def is_inactif(value, data=None):
	"""
	:param value: boolean
	:return: Oui/Non
	"""
	res = data
	if not value:
		if data:
			res = "<i class='fa fa-ban' style='color: red;'></i>&nbsp;<span class='text-secondary'>" + data + "</span>"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_total_records(total):
	"""
	Renvoie le nombre d'enregistrements
	"""
	res = ''
	if total > 1:
		res = "<strong style='color:#000;'>" + str(total) + "</strong><em class='text-primary'> enregistrements</em>"

	if total == 1:
		res = "<strong style='color:#000;'>" + str(total) + "</strong><em class='text-primary'> enregistrement</em>"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter(name='has_group')
def has_group(user, group_name):
	"""
	GESTION DES MENUS BASES PAR GROUP
	"""
	if not user:
		return False

	group = Group.objects.get(name=group_name)

	return True if group in user.groups.all() else False

#------------------------------------------------------------
@register.filter()
def get_user_current_group(user):
	"""
	Renvoie le nom du group de l'utilisateur en cours
	"""
	try:
		res = " -<strong class='text-light'>&nbsp;Service " + user.groups.all()[0].name.capitalize() + "&nbsp;</strong>" 
	except:
		res = " -<strong class='text-light'>&nbsp;Administrateur&nbsp;</strong>"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_info_object(obj):
	"""
	Renvoie quelques info  de la classe (via l'instance obj)
	"""
	info = re.findall('[A-Z][^A-Z]*', obj.__class__.__name__)
	res = ''
	for elt in info:
		res += ' ' + str(elt)

	res = "'<strong><em>" + res.strip().capitalize() + "</em></strong>'"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_user_avatar(user):
	"""
	Renvoie le chemin complète de l'avatar de l'utilisateur'
	"""
	res = '/static/img/photo.jpg'
	if isinstance(user, User):
		# try:
		# 	obj = Employe.objects.get(pk=user.pk)
		# 	if obj and obj.avatar:
		# 		return settings.MEDIA_URL + str(obj.avatar)
		# except:
			pass

	return res

#------------------------------------------------------------
@register.filter()
def show_user_name(user):
	"""
	Renvoie le prénom de l'utilisateur
	"""
	if isinstance(user, User):
		if user.is_superuser:
			return user.username
		if user.first_name:
			return user.first_name
		elif user.last_name:
			return user.last_name
	else:
		return ''

#------------------------------------------------------------
@register.filter()
def to_wrap(text, number):
	"""
	Allow long words to be able to break and wrap onto the next line
	@text: text to wrap
	@number: number of the word in each line
	"""
	MOTS = number
	lst = text.split(' ')
	i = 1
	s = ""
	mots = []
	passed = False
	for e in lst:
		s += " " + e
		if i == MOTS:
			passed = True
			mots.append(s.strip())
			i = 1
			s = ""
		i = i + 1
		
	if passed==False:
		mots.append(text)
	elif len(s.split()) > 0:
		mots.append(s)

	res = ""
	for m in mots:
		res += "<span>" + m + "</span>" + "<br>"

	return mark_safe(res)