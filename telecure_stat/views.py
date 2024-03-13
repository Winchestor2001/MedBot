from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from med_app.models import *
from django.db.models import Sum


@login_required
def home_page(request):
    total_members = User.objects.all().count()
    total_doctors = Doctor.objects.all().count()
    total_patients = Patient.objects.all().count()
    doctors_earn = Doctor.objects.all().aggregate(total_balance=Sum('balance'))
    total_balance = doctors_earn['total_balance'] if doctors_earn['total_balance'] else 0
    doctors = Doctor.objects.all().order_by('-balance')

    context = {
        "total_members": total_members,
        "total_doctors": total_doctors,
        "total_patients": total_patients,
        "total_doctor_balance": total_balance,
        "doctors": doctors,
    }

    return render(request, 'index.html', context=context)
