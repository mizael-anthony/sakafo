from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.utils.encoding import force_bytes
# Create your views here.
import  stripe
import math
import pytz

from reservation.templates import ReservationDemandeTemplate
from reservation.models import Reservation_Demande
from livraisons.models import Livraison
from livraisons.templates import LivraisonTemplate

from flottes.models import Flotte
from flottes.templates import FlotteTemplate

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url="/login/")
def charge(request):
    if request.method == 'POST':
        reservation_id = request.POST["reservation_id"]
        reservation = Reservation_Demande.objects.get(id = reservation_id)
        prix = reservation.prix * 100
        charge = stripe.Charge.create(
            amount=math.floor(prix),
            currency='eur',
            description='Réservation à la demande',
            source=request.POST['stripeToken']
        )
        if charge.paid:
            reservation.statut = 1
            reservation.charge = charge.id
            reservation.save(force_update=True)
            associated_users = User.objects.filter(Q(email=settings.EMAIL_RESERVATION))
            if associated_users.exists():
                tz_France = pytz.timezone('Europe/Paris')
                d_aware = reservation.date_created.astimezone(tz_France)
                for user in associated_users:
                    subject = "Allocation de voiture - Réservation à la demande"
                    email_template_name = "reservation_demande/allocation_voiture.txt"
                    c = {
                    "email":user.email,
                    'type':reservation.get_type_display(),
                    'site_name': 'i-mobility',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'client': reservation.client,
                    'date': d_aware.strftime("%d/%m/%Y - %H:%M:%S"),
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'infrastructure@inhome-insol.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('En-tête invalide.')
        # return render(request, 'charge.html')
        html_template = loader.get_template( ReservationDemandeTemplate.list )
        return HttpResponse(html_template.render(context={'reservations':Reservation_Demande.objects.filter(client__id = request.user.id), 'key':settings.STRIPE_PUBLISHABLE_KEY}, request=request))

@login_required(login_url="/login/")
def charge_livraison(request):
    if request.method == 'POST':
        livraison_id = request.POST["livraison_id"]
        livraison = Livraison.objects.get(id = livraison_id)
        prix = livraison.prix * 100
        charge = stripe.Charge.create(
            amount=math.floor(prix),
            currency='eur',
            description='Livraison',
            source=request.POST['stripeToken']
        )
        if charge.paid:
            livraison.statut = 1
            livraison.charge = charge.id
            livraison.save(force_update=True)
            associated_users = User.objects.filter(Q(email=settings.EMAIL_LIVRAISON))
            if associated_users.exists():
                tz_France = pytz.timezone('Europe/Paris')
                d_aware = livraison.date_created.astimezone(tz_France)
                for user in associated_users:
                    subject = "Allocation de voiture - Livraison"
                    email_template_name = "livraison/allocation_voiture.txt"
                    c = {
                    "email":user.email,
                    'site_name': 'i-mobility',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'client': livraison.client,
                    'date': d_aware.strftime("%d/%m/%Y - %H:%M:%S"),
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'infrastructure@inhome-insol.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('En-tête invalide.')
        # return render(request, 'charge.html')
        html_template = loader.get_template( LivraisonTemplate.list )
        return HttpResponse(html_template.render(context={'livraisons':Livraison.objects.filter(client__id = request.user.id), 'key':settings.STRIPE_PUBLISHABLE_KEY}, request=request))

@login_required(login_url="/login/")
def refund(request):
    if request.method == 'POST':
        reservation_id = request.POST["reservation_id"]
        reservation = Reservation_Demande.objects.get(id = reservation_id)
        prix = reservation.prix * 80
        refund = stripe.Refund.create(
            amount=math.floor(prix),
            charge=reservation.charge,
        )
        if refund.status == "succeeded":
            reservation.statut = 2
            reservation.save(force_update=True)
        # return render(request, 'charge.html')
        html_template = loader.get_template( ReservationDemandeTemplate.list )
        return HttpResponse(html_template.render(context={'reservations':Reservation_Demande.objects.filter(client__id = request.user.id), 'key':settings.STRIPE_PUBLISHABLE_KEY}, request=request))

@login_required(login_url="/login/")
def refund_livraison(request):
    if request.method == 'POST':
        livraison_id = request.POST["livraison_id"]
        livraison = Livraison.objects.get(id = livraison_id)
        prix = livraison.prix * 80
        refund = stripe.Refund.create(
            amount=math.floor(prix),
            charge=livraison.charge,
        )
        if refund.status == "succeeded":
            livraison.statut = 2
            livraison.save(force_update=True)
        # return render(request, 'charge.html')
        html_template = loader.get_template( LivraisonTemplate.list )
        return HttpResponse(html_template.render(context={'livraisons':Livraison.objects.filter(client__id = request.user.id), 'key':settings.STRIPE_PUBLISHABLE_KEY}, request=request))

@login_required(login_url="/login/")
def charge_location(request):
    if request.method == 'POST':
        flotte_id = request.POST["obj_id"]
        flotte = Flotte.objects.get(id = flotte_id)
        prix = flotte.get_total * 100
        charge = stripe.Charge.create(
            amount=math.floor(prix),
            currency='eur',
            description='Location de flottes',
            source=request.POST['stripeToken']
        )
        if charge.paid:
            flotte.statut = 1
            flotte.charge = charge.id
            flotte.save(force_update=True)
            associated_users = User.objects.filter(Q(email=settings.EMAIL_LOCATION))
            if associated_users.exists():
                tz_France = pytz.timezone('Europe/Paris')
                d_aware = flotte.date_created.astimezone(tz_France)
                for user in associated_users:
                    subject = "Allocation de véhicules - Location de flottes"
                    email_template_name = "flotte/allocation.txt"
                    c = {
                    "email":user.email,
                    'debut':flotte.debut,
                    'fin':flotte.fin,
                    'site_name': 'i-mobility',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'client': flotte.client,
                    'date': d_aware.strftime("%d/%m/%Y - %H:%M:%S"),
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'infrastructure@inhome-insol.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('En-tête invalide.')
        # return render(request, 'charge.html')
        html_template = loader.get_template( FlotteTemplate.index )
        lst = Flotte.objects.filter(client__id = request.user.id).order_by('date_created')
        if request.user.is_superuser:
            lst = Flotte.objects.all().order_by('date_created')
        total = lst.count

        context = {
            'lst': lst,
            'total': total,
            'key':settings.STRIPE_PUBLISHABLE_KEY,
        }
        return HttpResponse(html_template.render(context, request=request))

@login_required(login_url="/login/")
def refund_location(request):
    if request.method == 'POST':
        flotte_id = request.POST["obj_id"]
        flotte = Flotte.objects.get(id = flotte_id)
        prix = flotte.get_total * 80
        refund = stripe.Refund.create(
            amount=math.floor(prix),
            charge=flotte.charge,
        )
        if refund.status == "succeeded":
            flotte.statut = 2
            flotte.save(force_update=True)
        # return render(request, 'charge.html')
        html_template = loader.get_template( FlotteTemplate.index )
        lst = Flotte.objects.filter(client__id = request.user.id).order_by('date_created')
        if request.user.is_superuser:
            lst = Flotte.objects.all().order_by('date_created')
        total = lst.count
        context = {
            'lst': lst,
            'total': total,
            'key':settings.STRIPE_PUBLISHABLE_KEY,
        }
        return HttpResponse(html_template.render(context, request=request))