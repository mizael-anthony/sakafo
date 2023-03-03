from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

#------------------------------------------------------------
@register.filter()
def get_stripe_price(value):
	"""Load photo profil"""

	return value * 100
#------------------------------------------------------------
@register.filter()
def get_stripe_refund_price(value):
	"""Load photo profil"""

	return value * 0.8

#------------------------------------------------------------
@register.filter()
def nb_colis(value):
	"""Load photo profil"""
	nb = 0
	if value.colis_1:
		nb = nb + 1
	if value.colis_2:
		nb = nb + 1
	if value.colis_3:
		nb = nb + 1
	if value.colis_4:
		nb = nb + 1
	return nb
