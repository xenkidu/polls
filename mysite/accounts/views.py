from django.shortcuts import render
from django.views import generic


def index_view(request):
    context = {}
    return render(request, 'accounts/index.html', context)