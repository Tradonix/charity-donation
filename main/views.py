from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from accounts.models import User
from main.models import Category, Institution, Donation


class LandingPage(View):
    def get(self, request):
        context = {
            'fundacje': Institution.objects.filter(type__exact='FU'),
            'organizacje': Institution.objects.filter(type__exact='OP'),
            'zbiorki': Institution.objects.filter(type__exact='ZL'),
        }
        return render(request, 'index.html', context)


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        context = {'categories': Category.objects.all(),
                   'institutions': Institution.objects.all()}
        return render(request, 'form.html', context)

    def post(self, request):
        quantity = request.POST.get('bags')
        institution = ""
        if request.POST.get('organization'):
            institution = Institution.objects.get(pk=request.POST.get('organization'))
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('date')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user = request.user

        if quantity and institution and address and phone_number and city and zip_code and pick_up_date and pick_up_time and user:
            dono = Donation.objects.create(
                quantity=quantity,
                institution=institution,
                address=address,
                phone_number=phone_number,
                city=city,
                zip_code=zip_code,
                pick_up_date=pick_up_date,
                pick_up_time=pick_up_time,
                pick_up_comment=pick_up_comment,
                user=user
            )

            dono.categories.set(request.POST.getlist('categories'))  # m2m
            dono.save()
            return HttpResponse(reverse_lazy('done_donation'))

        return HttpResponse('bląd, conij i popraw', status=500)


class DoneDonation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')
