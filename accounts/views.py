from accounts.forms import MyUserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView


class Register(CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'registration/register.html'


class Login(LoginView):
    template_name = 'registration/login.html'

