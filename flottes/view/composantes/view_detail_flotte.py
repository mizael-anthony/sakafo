from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from flottes.models import Flotte, DetailFlotte
from flottes.forms import DetailFlotteForm
from flottes.templates import ComposanteTemplate
from reservation.models import Tarif

from helpers.hlp_error import ErrorsHelpers

def detail_flotte_crud(request, pk_flotte):
    obj = get_object_or_404(Flotte, pk=pk_flotte)
    details = DetailFlotte.objects.filter(flotte__id=pk_flotte)

    form = DetailFlotteForm()
    context = {'obj': obj, 'details': details, 'form': form, 'tarif':Tarif.objects.first()}

    data = dict()
    data['html_form'] = render_to_string(ComposanteTemplate.detail_flotte_crud, context, request=request)

    return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def detail_flotte_create(request):
    """
    Création/Ajout des details
    """
    # Recuprer les valeurs des élémens html du formulaire
    pk = request.POST["id_flotte"]
    quantite = request.POST["id_quantite"]
    type = request.POST["id_type"]

    obj = get_object_or_404(Flotte, pk=pk)
    data = dict()

    try:            
        detail = DetailFlotte()

        detail.flotte = obj
        detail.type = type
        detail.quantite = quantite 
        if detail.type == '0':
            detail.prix = Tarif.objects.first().daily_cost * Tarif.objects.first().electric_coef * int(quantite)
        if detail.type == '1':
            detail.prix = Tarif.objects.first().daily_cost * Tarif.objects.first().hybrid_coef * int(quantite)
        if detail.type == '2':
            detail.prix = Tarif.objects.first().daily_cost * Tarif.objects.first().shared_coef * int(quantite)
        if detail.type == '3':
            detail.prix = Tarif.objects.first().daily_cost * Tarif.objects.first().velo_coef * int(quantite)
        if detail.type == '4':
            detail.prix = Tarif.objects.first().daily_cost * Tarif.objects.first().trottinette_coef * int(quantite)

        detail.save()
    except Exception as e:
        data['error'] = e.message
    else:
        # Definir le context
        details = DetailFlotte.objects.filter(flotte_id=pk)
        form = DetailFlotteForm()
        context = {'obj': obj, 'details': details , 'form': form}

        data['html_content_list'] = render_to_string(ComposanteTemplate.detail_flotte_content, context, request=request)

    return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def detail_flotte_delete(request):
    """
    Suppression d'un detail
    """
    # Recuprer les valeurs des élémens html du formulaire
    pk = request.POST["id_flotte"]
    obj = get_object_or_404(Flotte, pk=pk)

    try:
        detail_id = request.POST["id_detail"]
        detail = get_object_or_404(DetailFlotte, pk=detail_id)
        detail.delete()
    except:
        return ErrorsHelpers.show_message(request, "Erreur de suppression des details.")

    # Definir le context
    details = DetailFlotte.objects.filter(flotte_id=pk)
    form = DetailFlotteForm()
    context = {'obj': obj, 'details': details , 'form': form}

    data = dict()
    data['html_content_list'] = render_to_string(ComposanteTemplate.detail_flotte_content, context, request=request)

    return JsonResponse(data)