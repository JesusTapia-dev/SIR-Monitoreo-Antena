from django.urls import path

from . import views

urlpatterns = (
    path('<int:id_conf>/', views.dds_rest_conf, name='url_dds_rest_conf'),
    path('<int:id_conf>/<int:message>/', views.dds_rest_conf, name='url_dds_rest_conf'),
    path('<int:id_conf>/edit/', views.dds_rest_conf_edit, name='url_edit_dds_rest_conf'),
)
