from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views import View

from main.models import Category, Institution


class LandingPage(View):
    def get(self, request):
        return render(request, 'index.html')


# class AddDonation(LoginRequiredMixin, View):
class AddDonation(View):
    def get(self, request):
        context = {'categories': Category.objects.all()}
        context['institutions'] = Institution.objects.all()
        return render(request, 'form.html', context)


# temporary
class DonationAdded(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')
