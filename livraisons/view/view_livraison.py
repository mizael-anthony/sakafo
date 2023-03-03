from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.utils.encoding import force_bytes
from django.db import transaction, IntegrityError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from ..templates import LivraisonTemplate
from reservation.models import Tarif, voiture_demande

from helpers.hlp_error import ErrorsHelpers
from django.views.decorators.csrf import csrf_exempt

from livraisons.forms import LivraisonForm
from ..templates import LivraisonTemplate
from ..models import Livraison
from django.conf import settings

import pytz
from django.core.files.storage import FileSystemStorage

from xhtml2pdf import pisa

@login_required(login_url="/login/")
def index(request):
	request.session['url_list'] = request.get_full_path()
	
	html_template = loader.get_template( LivraisonTemplate.index )
	return HttpResponse(html_template.render(context={'tarif':Tarif.objects.first()}, request=request))

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt
def livraison_create(request):
	if request.method == 'POST':
		form = LivraisonForm(request.POST)
	else:
		form = LivraisonForm()
	
	return save_form(request, form, LivraisonTemplate.create_livraison, 'create_livraison')

@login_required(login_url="/login/")
def list(request):
	request.session['url_list'] = request.get_full_path()
	html_template = loader.get_template( LivraisonTemplate.list )
	return HttpResponse(html_template.render(context={'livraisons':Livraison.objects.filter(client__id = request.user.id), 'key':settings.STRIPE_PUBLISHABLE_KEY}, request=request))

@login_required(login_url="/login/")
def detail(request,pk):
	request.session['url_list'] = request.get_full_path()
	livraison = Livraison.objects.get(pk = pk)
	html_template = loader.get_template( LivraisonTemplate.detail )
	return HttpResponse(html_template.render(context={'livraison':livraison,}, request=request))

#----------------------------------------------------------------
def save_form(request, form, template_name, action):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			try:
				with transaction.atomic():
					livraison = form.save(commit=False)
					livraison.client = request.user
					livraison.save()

			except IntegrityError as e:
				return ErrorsHelpers.show_message(request, "Erreur d'enregistrement de la livraison " + str(e))
			
			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(LivraisonTemplate.index, context={'tarif':Tarif.objects.first()})
			
			# Recharger la page pour faire apparaître le context-menu
			# data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	else:
		context = {'form': form, 'tarif':Tarif.objects.first()}
		data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
def view_livraison_pdf_invoice(request, pk):
	obj = Livraison.objects.filter(pk=pk).first()
	tz_France = pytz.timezone('Europe/Paris')
	d_aware = obj.date_created.astimezone(tz_France)
	filen ='Facture_livraison_' + obj.client.first_name + '_' + obj.client.last_name + '_' + d_aware.strftime("%d-%m-%Y") + '.pdf'
	fs = FileSystemStorage(location=str(settings.BASE_DIR) + '/static/pdf')
	context = {'livraison':obj,}
	html = render_to_string('livraison/livraison_pdf.html',context)
	write_to_file = open(str(settings.BASE_DIR) + '/static/pdf/' + 'Facture_livraison_' + obj.client.first_name + '_' + obj.client.last_name + '_' + d_aware.strftime("%d-%m-%Y") + '.pdf', "w+b")
	result = pisa.CreatePDF(html,dest=write_to_file)
	write_to_file.close()
	with fs.open(filen) as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="' + filen + '"'
		return response

@login_required(login_url="/login/")
def terminer_livraison(request):
    if request.method == 'POST':
        livraison_id = request.POST["livraison_id"]
        livraison = Livraison.objects.get(id = livraison_id)
        livraison.statut = 3
        livraison.save(force_update=True)
        # return render(request, 'charge.html')
        html_template = loader.get_template( LivraisonTemplate.list )
        return HttpResponse(html_template.render(context={'livraisons':[livraison,], 'key':settings.STRIPE_PUBLISHABLE_KEY}, request=request))

@login_required(login_url="/login/")
def list_driver(request):
	request.session['url_list'] = request.get_full_path()
	voiture = voiture_demande.objects.filter(chauffeur__id = request.user.id, disponible=True).first()
	livraisons = []
	if voiture:
		livraisons = Livraison.objects.filter(voiture__id = voiture.id)
	html_template = loader.get_template( LivraisonTemplate.list )
	return HttpResponse(html_template.render(context={'livraisons':livraisons, 'key':settings.STRIPE_PUBLISHABLE_KEY}, request=request))

#-------------------------------------------------------------------------------------------
@receiver(pre_save, sender=Livraison)
def car_allocated(sender, instance, **kwargs):
	if instance.id is None:
		pass
	else:
		old_livraison = Livraison.objects.get(id=instance.id)
		if (old_livraison.voiture is None and instance.voiture is None) or (old_livraison.voiture and instance.voiture is None) or (old_livraison.voiture and instance.voiture and old_livraison.voiture.id == instance.voiture.id):
			pass
		else: 
			voiture = voiture_demande.objects.get(id=instance.voiture.id)
			associated_users = User.objects.filter(Q(email=voiture.chauffeur.email))
			if associated_users.exists():
				nb_colis = 0
				if instance.colis_1:
					nb_colis += 1
				if instance.colis_2:
					nb_colis += 1
				if instance.colis_3:
					nb_colis += 1
				if instance.colis_4:
					nb_colis += 1
				for user in associated_users:
					subject = "Livraison à réaliser"
					email_template_name = "livraison/realisation.txt"
					c = {
					"email":user.email,
					'site_name': 'i-mobility',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'depart': instance.adresse_depart,
					'arrivee': instance.adresse_arrivee,
					'date': instance.date.strftime("%d/%m/%Y"),
					'heure': instance.depart,
					'colis':nb_colis,
					'aller': 'aller-retour' if instance.aller_retour else 'aller simple',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'infrastructure@inhome-insol.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('En-tête invalide.')
		