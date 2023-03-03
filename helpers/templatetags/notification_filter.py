from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models import Q


# ------------------- NOTIFICATIONS SYSTRAY ------------------

register = template.Library()

