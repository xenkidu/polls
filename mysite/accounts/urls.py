from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.index_view, name="register"),
]