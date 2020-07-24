from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from accounts.models import User


class Register(View):
    def get(self, request):
        return render(request, 'registration/register.html')

    def post(self, request):
        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password1 and password2 and password1 == password2 and not User.objects.filter(email=email):
            u = User.objects.create(first_name=first_name, last_name=last_name, email=email)
            u.set_password(password2)
            u.save()
            return redirect(reverse_lazy('login'))
        return render(request, 'registration/register.html')


class Login(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy("login")
