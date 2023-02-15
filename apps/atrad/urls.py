from django.urls import path

from . import views

urlpatterns = (
    path('<int:id_conf>/', views.atrad_conf, name='url_atrad_conf'),
    path('<int:id_conf>/edit/', views.atrad_conf_edit, name='url_edit_atrad_conf'),
)