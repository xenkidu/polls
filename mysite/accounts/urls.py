from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login_view.as_view(), name="login"),
    path('logout/', views.logout_view.as_view(), name="logout"),
    path('profile/', views.profile_view.as_view(), name="profile"),
]