from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt # Utiliser pour les methodes POST
from django.contrib.auth.models import User

from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.utils.encoding import force_bytes

from flottes.models import Flotte, AllocationFlotte, vehicule_flotte
from flottes.forms import AllocationFlotteForm
from flottes.templates import ComposanteTemplate

from helpers.hlp_error import ErrorsHelpers

import pytz

#----------------------------------------------------------------
#--------------------- COMPOSANTE: OBJECTIF ---------------------
#----------------------------------------------------------------
def allocation_flotte_crud(request, pk_flotte):
	"""
	Liste des details
	"""
	obj = get_object_or_404(Flotte, pk=pk_flotte)
	details = AllocationFlotte.objects.filter(flotte__id=pk_flotte)
	
	form = AllocationFlotteForm()
	context = { 'obj': obj, 'details': details , 'form': form }
	
	data = dict()	
	data['html_form'] = render_to_string(ComposanteTemplate.allocation_flotte_crud, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def allocation_flotte_create(request):
    """
    Création/Ajout des details
    """
    # Recuprer les valeurs des élémens html du formulaire
    pk = request.POST["id_flotte"]
    vehicule = request.POST["id_vehicule"]

    obj = get_object_or_404(Flotte, pk=pk)
    data = dict()

    try:            
        detail = AllocationFlotte()
        v = vehicule_flotte.objects.get(id=vehicule)
        detail.flotte = obj
        detail.vehicule = v

        detail.save()
        associated_users = User.objects.filter(Q(email=v.chauffeur.email))
        if associated_users.exists():
            tz_France = pytz.timezone('Europe/Paris')
            d_aware = obj.date_created.astimezone(tz_France)
            for user in associated_users:
                subject = "Location de flottes à réaliser"
                email_template_name = "flotte/realisation.txt"
                c = {
                "email":user.email,
                'debut':obj.debut,
                'fin':obj.fin,
                'site_name': 'i-mobility',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'client': obj.client,
                'date': d_aware.strftime("%d/%m/%Y - %H:%M:%S"),
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'infrastructure@inhome-insol.com' , [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('En-tête invalide.')
    except Exception as e:
        data['error'] = e.message
    else:
        # Definir le context
        details = AllocationFlotte.objects.filter(flotte_id=pk)
        form = AllocationFlotteForm()
        context = {'obj': obj, 'details': details , 'form': form}
        
        data['html_content_list'] = render_to_string(ComposanteTemplate.allocation_flotte_content, context, request=request)

    return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def allocation_flotte_delete(request):
    """
    Suppression d'un details
    """
    # Recuprer les valeurs des élémens html du formulaire
    pk = request.POST["id_flotte"]
    obj = get_object_or_404(Flotte, pk=pk)

    try:
        detail_id = request.POST["id_detail"]
        detail = get_object_or_404(AllocationFlotte, pk=detail_id)
        detail.delete()
    except:
        return ErrorsHelpers.show_message(request, "Erreur de suppression des details.")

    # Definir le context
    details = AllocationFlotte.objects.filter(flotte_id=pk)
    form = AllocationFlotteForm()
    context = {'obj': obj, 'details': details , 'form': form}

    data = dict()
    data['html_content_list'] = render_to_string(ComposanteTemplate.allocation_flotte_content, context, request=request)

    return JsonResponse(data)