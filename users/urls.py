from django.urls import path
from . import views

app_name = 'users'


urlpatterns = [
    path('register/', views.register_user, name = 'register-user'),
    path('login/', views.login_user, name = 'login-user'),
    path('logout/', views.logout_user, name = 'logout-user'),
    
]
