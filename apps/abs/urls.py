from django.urls import path

from apps.abs import views

urlpatterns = (
    path('<int:id_conf>/', views.abs_conf, name='url_abs_conf'),
    path('<int:id_conf>/edit/', views.abs_conf_edit, name='url_edit_abs_conf'),
    path('alert/', views.abs_conf_alert, name='url_alert_abs_conf'),
    path('<int:id_conf>/import/', views.import_file, name='url_import_abs_conf'),
    #url(r'^(?P<id_conf>-?\d+)/status/', views.abs_conf, {'status_request':True},name='url_status_abs_conf'),
    path('<int:id_conf>/change_beam/<int:id_beam>/', views.send_beam, name='url_send_beam'),
    path('<int:id_conf>/plot/', views.plot_patterns, name='url_plot_abs_patterns'),
    path('<int:id_conf>/plot/<int:id_beam>/', views.plot_patterns, name='url_plot_abs_patterns2'),
    path('<int:id_conf>/plot/<int:id_beam>/<slug:antenna>/pattern.png/', views.plot_pattern, name='url_plot_beam'),
    path('<int:id_conf>/add_beam/', views.add_beam, name='url_add_abs_beam'),
    path('<int:id_conf>/beam/<int:id_beam>/delete/', views.remove_beam, name='url_remove_abs_beam'),
    path('<int:id_conf>/beam/<int:id_beam>/edit/', views.edit_beam, name='url_edit_abs_beam'),
)
