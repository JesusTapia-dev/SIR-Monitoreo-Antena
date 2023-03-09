from django.urls import path

from . import views

urlpatterns = (
    path('prueba/', views.atrad_prueba, name='url_prueba'),
    path('<int:id_conf>/', views.atrad_conf, name='url_atrad_conf'),
    path('<int:id_conf>/edit/', views.atrad_conf_edit, name='url_edit_atrad_conf'),
    path('<int:id_conf>/<slug:id_tx>/', views.atrad_tx, name='url_tx_atrad'),
)