from django import template
from django.utils.safestring import mark_safe

from datetime import datetime
register = template.Library()

#------------------------------------------------------------
@register.filter()
def get_total(value):
	"""Load photo profil"""

	return value.get_total

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
