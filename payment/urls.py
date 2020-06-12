from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    # path('process/', views.payment_process, name='process'),
    # path('done/', views.payment_done, name='done'),


    path('', views.index, name='index'),
    path('charge/', views.charge, name='charge'),
    path('success/<str:args>/', views.success, name='success'),
    path('canceled/', views.payment_canceled, name='canceled'),
]
