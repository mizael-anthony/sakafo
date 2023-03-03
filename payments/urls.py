from django.urls import path

from . import views

urlpatterns = [
    path('charge/', views.charge, name='charge'),
    path('refund/', views.refund, name='refund'),
    path('charge_livraison/', views.charge_livraison, name='charge_livraison'),
    path('charge_location/', views.charge_location, name='charge_location'),
    path('refund_location/', views.refund_location, name='refund_location'),
    path('refund_livraison/', views.refund_livraison, name='refund_livraison'),
]