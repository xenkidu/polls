from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages

from .forms import UserRegisterForm

def index_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('polls:index')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
