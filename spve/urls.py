from django.urls import path
from . import views

urlpatterns = [
    path('demo', views.demo_page),
    path('login', views.login_page),
    path('loggedin', views.logged_in),
    path('userdetails', views.user_details),
    path('logout', views.logout_user)
]
