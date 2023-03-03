"""i-mobility URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path 
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView 
from .forms import LoginForm
from .views import index, password_reset_request
from . import views 
 

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),

    # Admin
    path('i-mobility/admin/', admin.site.urls),
    path('i-mobility/admin/', lambda _: redirect('admin:index'), name='index_admin'),

   
	path('login/', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),

    path('login/', LoginView.as_view(), {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	path('logout/',LogoutView.as_view(), {'next_page': '/login'}),

    path("password_reset", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),      

    # path('accounts/', include('django.contrib.auth.urls')),
    path("register", views.register_request, name="register"),
    path("register_client", views.register_client_request, name="register_client"),

    path('reservation/', include('reservation.urls')),
    path('livraisons/', include('livraisons.urls')),
    path('actu/', include('actu.urls')),
    path('accounts/', include('allauth.urls')),
    path('payment/', include('payments.urls')),
    path('flotte/', include('flottes.urls')),

]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)