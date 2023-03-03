from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm, NewClientForm
from django.contrib.auth import login
from django.contrib import messages
from actu.models import Blog, Category
import datetime

@csrf_exempt
def index(request):
	request.session['url_list'] = request.get_full_path()
	cat = Category.objects.all()
	context = {
		'categories': Category.objects.all(),
		'posts': Blog.objects.all()[:6]
	}
	return render(request, 'home.html', context)

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			messages.success(request, "Enregistrement réussie." )
			return redirect("index")
		messages.error(request, "Echec de l'enregistrement, informations invalides.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})

def register_client_request(request):
	if request.method == "POST":
		form = NewClientForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			messages.success(request, "Enregistrement réussie." )
			return redirect("index")
		messages.error(request, "Echec de l'enregistrement, informations invalides.")
	form = NewClientForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Demande de réinitialisation de mot de passe"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'51.254.197.129',
                    'site_name': 'i-mobility',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'infrastructure@inhome-insol.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('En-tête invalide.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})