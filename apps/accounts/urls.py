from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = (
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='url_logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='url_login'),
)
