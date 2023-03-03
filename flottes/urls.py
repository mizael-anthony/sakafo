from django.urls import path
from django.contrib.auth.views import LoginView
from .import views

urlpatterns = [
	#-----------------------------------------------------
	#------------------- CRUD FLOTTE ---------------------
	#-----------------------------------------------------
	path('flotte/', views.flotte_list, name='flotte_list'),
	path('flotte/create', views.flotte_create, name='flotte_create'),
	path('flotte/<int:pk>/update', views.flotte_update, name='flotte_update'),
	path('flotte/terminer', views.terminer_location, name='terminer_location'),
	path('flotte/virement_recu', views.virement_recu, name='virement_recu'),
	path('flotte/<int:pk>/view_pdf_invoice/', views.view_location_pdf_invoice, name='view_location_pdf_invoice'),
	path('flotte/<int:pk_flotte>/virement/', views.virement, name='virement'),

	#-----------------------------------------------------
	#----------------- CRUD COMPOSANTES ------------------
	#-----------------------------------------------------
	# Composante: Detail Flotte
	path('flotte/<int:pk_flotte>/composantes/detail_flotte_crud/', views.detail_flotte_crud, name='detail_flotte_crud'),
	path('flotte/composantes/detail_flotte_create/', views.detail_flotte_create, name='detail_flotte_create'),
	path('flotte/composantes/detail_flotte_delete/', views.detail_flotte_delete, name='detail_flotte_delete'),

	# Composante: Besoin Formation
	path('flotte/<int:pk_flotte>/composantes/allocation_flotte_crud/', views.allocation_flotte_crud, name='allocation_flotte_crud'),
	path('flotte/composantes/allocation_flotte_create/', views.allocation_flotte_create, name='allocation_flotte_create'),
	path('flotte/composantes/allocation_flotte_delete/', views.allocation_flotte_delete, name='allocation_flotte_delete'),

	#-----------------------------------------------------
	#--------------------- LOGIN URL ---------------------
	#-----------------------------------------------------	
	# Login page !!! IMPORTANT !!!client_deactivate
	path('flotte/login/', LoginView.as_view(template_name='registration/login.html'), name="login"),
]

