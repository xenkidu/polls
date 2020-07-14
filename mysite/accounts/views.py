from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You may now login.')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

class login_view(views.LoginView):
    template_name = 'accounts/login.html'

class logout_view(views.LogoutView):
    template_name = 'accounts/logout.html'

@method_decorator(login_required, name='dispatch')
class profile_view(views.TemplateView):
    template_name = 'accounts/profile.html'