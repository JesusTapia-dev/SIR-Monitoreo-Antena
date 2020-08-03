from django.urls import path

from . import views

urlpatterns = (
    path('<int:id_conf>/', views.cgs_conf, name='url_cgs_conf'),
    path('<int:id_conf>/edit/', views.cgs_conf_edit, name='url_edit_cgs_conf'),
)
