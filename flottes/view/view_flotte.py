from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Utiliser pour les methodes POST
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from django.urls import reverse


from flottes import views

from flottes.models import Flotte, DetailFlotte, AllocationFlotte
from flottes.templates import FlotteTemplate
from flottes.forms import FlotteForm

from helpers.hlp_error import ErrorsHelpers
from helpers.hlp_traceability import TraceabilityHelpers

from django.conf import settings

import pytz
from django.core.files.storage import FileSystemStorage

from xhtml2pdf import pisa

def get_context(request):
	lst = []
	lst = Flotte.objects.filter(client__id = request.user.id).order_by('date_created')
	if request.user.is_superuser:
		lst = Flotte.objects.all().order_by('date_created')
	total = lst.count

	context = {
		'lst': lst,
		'total': total,
		'key':settings.STRIPE_PUBLISHABLE_KEY,
	}

	return context

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt
def flotte_list(request):
	"""
	Liste des entretiens individuels
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Update, etc.)
	request.session['url_list'] = request.get_full_path()
	
	return render(request, FlotteTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt
def flotte_create(request):
	"""
	Desc: Création d'un entretien individuel de formation d'un employé
	@pk_employe: Identifiant de l'employé à entretenir
	"""
	if request.method == 'POST':
		form = FlotteForm(request.POST, user=TraceabilityHelpers.get_current_user(request)) # Save current user / set it in form
	else:
		form = FlotteForm()
	
	return save_form(request, form, FlotteTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def flotte_update(request, pk):
	"""
	Modification de l'information de l'entretien
	"""
	obj = get_object_or_404(Flotte, pk=pk)

	if request.method == 'POST':
		form = FlotteForm(request.POST, instance=obj)
	else:
		form = FlotteForm(instance=obj)
	
	return save_form(request, form, FlotteTemplate.update, 'update')

#----------------------------------------------------------------
def save_form(request, form, template_name, action):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			try:
				with transaction.atomic():
					if action == 'create':
						# Garder temporairement l'objet modèle du formulaire
						obj = form.save(commit=False)

						user = TraceabilityHelpers.get_current_user(request)
						obj.client = request.user

						# Sauvegarder l'objet evaluation
						obj.save()

					elif action == 'update':
						# TraceabilityHelpers.get_datetime_now()
						pass

			except IntegrityError as e:
				return ErrorsHelpers.show_message(request, "Erreur de création de l'entretien " + str(e))
			
			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(FlotteTemplate.index, context=get_context(request))
			
			# Recharger la page pour faire apparaître le context-menu
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	else:
		context = {'form': form}
		data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

@login_required(login_url="/login/")
def terminer_location(request):
	if request.method == 'POST':
		flotte_id = request.POST["obj_id"]
		flotte = Flotte.objects.get(id = flotte_id)
		flotte.statut = 3
		flotte.save(force_update=True)
		# return render(request, 'charge.html')
		html_template = loader.get_template( FlotteTemplate.index )
		return HttpResponse(html_template.render(context=get_context(request), request=request))

#----------------------------------------------------------------------------------------------
@login_required(login_url="/login/")
def virement_recu(request):
	if request.method == 'POST':
		flotte_id = request.POST["obj_id"]
		flotte = Flotte.objects.get(id = flotte_id)
		flotte.statut = 1
		flotte.save(force_update=True)
		# return render(request, 'charge.html')
		html_template = loader.get_template( FlotteTemplate.index )
		return HttpResponse(html_template.render(context=get_context(request), request=request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def view_location_pdf_invoice(request, pk):
	obj = Flotte.objects.filter(pk=pk).first()
	details = DetailFlotte.objects.filter(flotte__id=obj.id)
	tz_France = pytz.timezone('Europe/Paris')
	d_aware = obj.date_created.astimezone(tz_France)
	filen ='Facture_location_' + obj.client.first_name + '_' + obj.client.last_name + '_' + d_aware.strftime("%d-%m-%Y") + '.pdf'
	fs = FileSystemStorage(location=str(settings.BASE_DIR) + '/static/pdf')
	context = {'location':obj,'details':details}
	html = render_to_string('flotte/location_pdf.html',context)
	write_to_file = open(str(settings.BASE_DIR) + '/static/pdf/' + 'Facture_location_' + obj.client.first_name + '_' + obj.client.last_name + '_' + d_aware.strftime("%d-%m-%Y") + '.pdf', "w+b")
	result = pisa.CreatePDF(html,dest=write_to_file)
	write_to_file.close()
	with fs.open(filen) as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="' + filen + '"'
		return response

#---------------------------------------------------------------------
@login_required(login_url="login/")
def virement(request, pk_flotte):
	obj = get_object_or_404(Flotte, pk=pk_flotte)
	data = dict()
	if request.method == 'POST':
		try:
			with transaction.atomic():
				obj.mode_paiement = 1
				obj.save()

		except IntegrityError as e:
			return ErrorsHelpers.show_message(request, "Erreur de mise à jour du virement " + str(e))
			
		data['form_is_valid'] = True
		data['html_content_list'] = render_to_string(FlotteTemplate.index, context=get_context(request))
		
		data['url_redirect'] = request.session['url_list']
	else:
		context = {'email':settings.EMAIL_VIREMENT, 'obj': obj}
		data['html_form'] = render_to_string(FlotteTemplate.virement, context, request=request)

	return JsonResponse(data)


