from django.urls import path

from . import views

urlpatterns = (
    path('<int:id_conf>/', views.jars_conf, name='url_jars_conf'),
    path('<int:id_conf>/edit/', views.jars_conf_edit, name='url_edit_jars_conf'),    
    path('<int:conf_id>/change_filter/', views.change_filter, name='url_change_jars_filter'),
    path('<int:conf_id>/change_filter/<int:filter_id>/', views.change_filter, name='url_change_jars_filter'),
    path('<int:conf_id>/new_filter/', views.new_filter, name='url_new_jars_filter'),
    path('<int:conf_id>/import/', views.import_file, name='url_import_jars_conf'),
    path('<int:conf_id>/read/', views.read_conf, name='url_read_jars_conf'),
    path('<int:conf_id>/get_log/', views.get_log, name='url_get_jars_log'),
)
