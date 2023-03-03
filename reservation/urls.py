from django.urls import path

from . import views

urlpatterns = [
    path('reservation_demande', views.index, name='reservation_demande'),
    path('reservation_demande/list', views.list, name='reservation_demande_list'),
    path('reservation_demande/detail/<int:pk>', views.detail, name='reservation_demande_detail'),
    path('reservation_demande/<int:pk>/view_pdf_invoice/', views.view_pdf_invoice, name='view_pdf_invoice'),
    path('reservation_demande/terminer', views.terminer, name='terminer'),
    path('reservation_demande/list_driver', views.list_driver, name='reservation_demande_list_driver'),
    path('reservation_reguliere', views.index_reguliere, name='reservation_reguliere'),
    path('reservation_demande/shared_reservation_create', views.shared_reservation_create, name='shared_reservation_create'),
    path('reservation_demande/electric_reservation_create', views.electric_reservation_create, name='electric_reservation_create'),
    path('reservation_demande/hybrid_reservation_create', views.hybrid_reservation_create, name='hybrid_reservation_create'),
]