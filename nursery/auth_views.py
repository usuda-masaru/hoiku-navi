from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    template_name = 'nursery/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('nursery:nursery_list')


class CustomLogoutView(LogoutView):
    next_page = 'nursery:login'


def signup(request):
    if request.user.is_authenticated:
        return redirect('nursery:nursery_list')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('nursery:nursery_list')
    else:
        form = UserCreationForm()
    return render(request, 'nursery/signup.html', {'form': form})