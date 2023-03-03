from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.utils.encoding import force_bytes
from django.db import transaction, IntegrityError
from django.views.generic.edit import CreateView
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from ..models import Tarif, Ligne_reguliere, Reservation_Demande, voiture_demande

from ..templates import ReservationDemandeTemplate, ReservationReguliereTemplate
import requests
import facebook as fb
import pytz
from django.core.files.storage import FileSystemStorage


from helpers.hlp_error import ErrorsHelpers
from django.views.decorators.csrf import csrf_exempt

from datetime import timedelta

from reservation.forms import ReservationDemandeForm

from xhtml2pdf import pisa

@login_required(login_url="/login/")
def index(request):
	request.session['url_list'] = request.get_full_path()
	# url = f"https://graph.facebook.com/507842821104882/accounts?fields=name, access_token, picture, id&access_token=507842821104882|whk9u67EtPQwyECp8cMEDk9_Muw"
	# response = requests.get(url)
	# data = response.json()
	
	# url1 = f"https://graph.facebook.com/112602591681595/feed?message=Hello&access_token=EAAHN4V70JPIBADdhVFHihqbttFIOooop7nnDXAZBq1YXCWUbrrZCXuerGcpB0eHOVIp4XVEoCWIuV7NwZAQZB0ci4rB5VEOaacS3tTxwZC9kMOc9Tu994q3MZADQZBCZCD9tARbrP1pj5ZAo9uXvzUcP9ZAR025QPleR41geZAaFwfqds9OaIkvoUL9BCydAzDw41n6ru3aIXZBjLdae5oabc19C"
	# resp = requests.get(url1)

	access_token = "EAAHN4V70JPIBAPwFFyHFYUZAexNelW5I8Pt1BZC57ZB4YT1ZB7hk1xtHUWiYrkDvUWIYHwwfkEAydhZAZCVBSQaiCISA1KDGar7PfM9oKAtJmAFWfMLcYwMejKnjWbZCMgqLPK4F5VtQc79fha5K7n5nEQuNquPb4HOWZAaJgLAKx8hPNokTc4TlEMstrHn8NJq4OrPZAik3ZBqAZDZD"
	faceb = fb.GraphAPI(access_token)
	# faceb.put_object("me","feed",message = "Bonjour, IMOBILITYTECHNOLOGIES est là!")
	html_template = loader.get_template( ReservationDemandeTemplate.index )
	return HttpResponse(html_template.render(context={'tarif':Tarif.objects.first()}, request=request))

@login_required(login_url="/login/")
def list(request):
	request.session['url_list'] = request.get_full_path()
	html_template = loader.get_template( ReservationDemandeTemplate.list )
	return HttpResponse(html_template.render(context={'reservations':Reservation_Demande.objects.filter(client__id = request.user.id), 'key':settings.STRIPE_PUBLISHABLE_KEY}, request=request))

@login_required(login_url="/login/")
def detail(request,pk):
	request.session['url_list'] = request.get_full_path()
	reservation = Reservation_Demande.objects.get(pk = pk)
	html_template = loader.get_template( ReservationDemandeTemplate.detail )
	return HttpResponse(html_template.render(context={'reservation':reservation,}, request=request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def view_pdf_invoice(request, pk):
	obj = Reservation_Demande.objects.filter(pk=pk).first()
	tz_France = pytz.timezone('Europe/Paris')
	d_aware = obj.date_created.astimezone(tz_France)
	filen ='Facture_res_dde_' + str(obj.get_type_display()) + '_' + obj.client.first_name + '_' + obj.client.last_name + '_' + d_aware.strftime("%d-%m-%Y") + '.pdf'
	fs = FileSystemStorage(location=str(settings.BASE_DIR) + '/static/pdf')
	context = {'reservation':obj,}
	html = render_to_string('reservation_demande/reservation_demande_pdf.html',context)
	write_to_file = open(str(settings.BASE_DIR) + '/static/pdf/' + 'Facture_res_dde_' + str(obj.get_type_display()) + '_' + obj.client.first_name + '_' + obj.client.last_name + '_' + d_aware.strftime("%d-%m-%Y") + '.pdf', "w+b")
	result = pisa.CreatePDF(html,dest=write_to_file)
	write_to_file.close()
	with fs.open(filen) as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="' + filen + '"'
		return response

@login_required(login_url="/login/")
def terminer(request):
    if request.method == 'POST':
        reservation_id = request.POST["reservation_id"]
        reservation = Reservation_Demande.objects.get(id = reservation_id)
        reservation.statut = 3
        reservation.save(force_update=True)
        # return render(request, 'charge.html')
        html_template = loader.get_template( ReservationDemandeTemplate.list )
        return HttpResponse(html_template.render(context={'reservations':[reservation,], 'key':settings.STRIPE_PUBLISHABLE_KEY}, request=request))

@login_required(login_url="/login/")
def list_driver(request):
	request.session['url_list'] = request.get_full_path()
	voiture = voiture_demande.objects.filter(chauffeur__id = request.user.id, disponible=True).first()
	reservations = []
	if voiture:
		reservations = Reservation_Demande.objects.filter(voiture__id = voiture.id)
	html_template = loader.get_template( ReservationDemandeTemplate.list )
	return HttpResponse(html_template.render(context={'reservations':reservations, 'key':settings.STRIPE_PUBLISHABLE_KEY}, request=request))

@login_required(login_url="/login/")
def index_reguliere(request):
	request.session['url_list'] = request.get_full_path()
	html_template = loader.get_template( ReservationReguliereTemplate.index )
	return HttpResponse(html_template.render(context={'lignes':Ligne_reguliere.objects.all()}, request=request))

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt
def shared_reservation_create(request):
	if request.method == 'POST':
		form = ReservationDemandeForm(request.POST)
	else:
		form = ReservationDemandeForm(type=request.GET.get('type',''))
	
	return save_form(request, form, ReservationDemandeTemplate.create_shared, 'create_shared')

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt
def electric_reservation_create(request):
	if request.method == 'POST':
		form = ReservationDemandeForm(request.POST)
	else:
		form = ReservationDemandeForm(type=request.GET.get('type',''))
	
	return save_form(request, form, ReservationDemandeTemplate.create_electric, 'create_electric')

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt
def hybrid_reservation_create(request):
	if request.method == 'POST':
		form = ReservationDemandeForm(request.POST)
	else:
		form = ReservationDemandeForm(type=request.GET.get('type',''))
	
	return save_form(request, form, ReservationDemandeTemplate.create_hybrid, 'create_hybrid')

#----------------------------------------------------------------
def save_form(request, form, template_name, action):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			try:
				with transaction.atomic():
					reservation = form.save(commit=False)
					reservation.client = request.user
					reservation.save()

			except IntegrityError as e:
				return ErrorsHelpers.show_message(request, "Erreur d'enregistrement de la réservation " + str(e))
			
			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(ReservationDemandeTemplate.index, context={'tarif':Tarif.objects.first()})
			
			# Recharger la page pour faire apparaître le context-menu
			# data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	else:
		context = {'form': form}
		data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

#-------------------------------------------------------------------------------------------
@receiver(pre_save, sender=Reservation_Demande)
def car_allocated(sender, instance, **kwargs):
	if instance.id is None:
		pass
	else:
		old_reservation = Reservation_Demande.objects.get(id=instance.id)
		if (old_reservation.voiture is None and instance.voiture is None) or (old_reservation.voiture and instance.voiture is None) or (old_reservation.voiture and instance.voiture and old_reservation.voiture.id == instance.voiture.id):
			pass
		else: 
			voiture = voiture_demande.objects.get(id=instance.voiture.id)
			associated_users = User.objects.filter(Q(email=voiture.chauffeur.email))
			if associated_users.exists():
				for user in associated_users:
					subject = "Réservation à la demande à réaliser"
					email_template_name = "reservation_demande/realisation.txt"
					c = {
					"email":user.email,
					'type':instance.get_type_display(),
					'site_name': 'i-mobility',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'depart': instance.adresse_depart,
					'arrivee': instance.adresse_arrivee,
					'date': instance.date.strftime("%d/%m/%Y"),
					'heure': instance.depart,
					'passager': instance.nb_passager,
					'aller': 'aller-retour' if instance.aller_retour else 'aller simple',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'infrastructure@inhome-insol.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('En-tête invalide.')
			



	