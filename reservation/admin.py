from django.contrib import admin
from .models import Address, Tarif, Ligne_reguliere, Reservation_Demande, voiture_demande

# Register your models here.
admin.site.register(Address)
admin.site.register(Tarif)
admin.site.register(Ligne_reguliere)
admin.site.register(Reservation_Demande)
admin.site.register(voiture_demande)