from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('<int:question_id>/', views.detail_view, name='detail'),
    path('<int:question_id>/results/', views.results_view, name='results'),
    path('<int:question_id>/vote/', views.vote_view, name='vote'),
]
