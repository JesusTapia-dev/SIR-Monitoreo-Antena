from django.urls import path

from apps.main import views

urlpatterns = (
    path('<int:id_conf>/', views.dev_conf, name='url_usrp_conf'),
    path('<int:id_conf>/edit/', views.dev_conf_edit, name='url_edit_usrp_conf'),
    path('<int:id_conf>/write/', views.dev_conf_write, name='url_write_usrp_conf'),
    path('<int:id_conf>/read/', views.dev_conf_read, name='url_read_usrp_conf'),
    path('<int:id_conf>/import/', views.dev_conf_import, name='url_import_usrp_conf'),
    path('<int:id_conf>/export/', views.dev_conf_export, name='url_export_usrp_conf'),
)
