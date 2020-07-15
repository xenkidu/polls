from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm


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

    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, self.template_name, {'u_form': u_form,'p_form': p_form})

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            # <process form cleaned data>
            u_form.save()
            p_form.save()
            messages.success(request, f'Account Updated!')
            return redirect('accounts:profile')

        return render(request, self.template_name, {'u_form': u_form, 'p_form': p_form})