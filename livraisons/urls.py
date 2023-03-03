from django.urls import path

from . import views

urlpatterns = [
    path('livraison', views.index, name='livraison'),
    path('livraison/livraison_create', views.livraison_create, name='livraison_create'),
    path('livraison/list', views.list, name='livraison_list'),
    path('livraison/detail/<int:pk>', views.detail, name='livraison_detail'),
    path('livraison/<int:pk>/view_pdf_invoice/', views.view_livraison_pdf_invoice, name='view_livraison_pdf_invoice'),
    path('livraison/terminer', views.terminer_livraison, name='terminer_livraison'),
    path('livraison/list_driver', views.list_driver, name='livraison_list_driver'),
    
]