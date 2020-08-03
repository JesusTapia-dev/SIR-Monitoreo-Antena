from django.urls import path

from . import views

urlpatterns = (
    path('<int:conf_id>/', views.conf, name='url_rc_conf'),
    path('<int:conf_id>/import/', views.import_file, name='url_import_rc_conf'),
    path('<int:conf_id>/edit/', views.conf_edit, name='url_edit_rc_conf'),
    path('<int:conf_id>/plot/', views.plot_pulses, name='url_plot_rc_pulses'),
    path('<int:conf_id>/plot2/', views.plot_pulses2, name='url_plot_rc_pulses2'),
    #url(r'^(?P<id_conf>-?\d+)/write/$', 'apps.main.views.dev_conf_write', name='url_write_rc_conf'),
    #url(r'^(?P<id_conf>-?\d+)/read/$', 'apps.main.views.dev_conf_read', name='url_read_rc_conf'),
    path('<int:conf_id>/raw/', views.conf_raw, name='url_raw_rc_conf'),
    path('<int:conf_id>/add_line/', views.add_line, name='url_add_rc_line'),
    path('<int:conf_id>/add_line/<int:line_type_id>/', views.add_line, name='url_add_rc_line'),
    path('<int:conf_id>/add_line/<int:line_type_id>/code/<int:code_id>/', views.add_line, name='url_add_rc_line_code'),
    path('<int:conf_id>/update_position/', views.update_lines_position, name='url_update_rc_lines_position'),
    path('<int:conf_id>/line/<int:line_id>/delete/', views.remove_line, name='url_remove_rc_line'),
    path('<int:conf_id>/line/<int:line_id>/add_subline/', views.add_subline, name='url_add_rc_subline'),
    path('<int:conf_id>/line/<int:line_id>/codes/', views.edit_codes, name='url_edit_rc_codes'),
    path('<int:conf_id>/line/<int:line_id>/codes/<int:code_id>/', views.edit_codes, name='url_edit_rc_codes'),
    path('<int:conf_id>/line/<int:line_id>/subline/<int:subline_id>/delete/', views.remove_subline, name='url_remove_rc_subline'),
)
