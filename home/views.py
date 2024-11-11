from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .forms import TokenForm
from .models import *



def create_token(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        doctor = User.objects.get(pk=doctor_id) 
        token = request.POST.get('token_no')
        phone_no = request.POST.get('phone_no')
        date = request.POST.get('available_date')
        time = request.POST.get('available_time')
        name = request.POST.get('patient_name')
        if PatientToken.objects.filter(doctor=doctor, phone_no=phone_no, date=date, time=time, name=name).exists():
            messages.error(request, f"Already Exists. Please try again with another details")
            return redirect('token-booking')
        PatientToken.objects.create(doctor=doctor, token_no=token, phone_no=phone_no, date=date, time=time, name=name)
        messages.success(request, f"Your Token number is {token}. please note the token number!")
        return redirect('token-booking')
    else:
        return render(request, 'index.html')
    


def doctor_list(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        date = request.POST.get('date')
        available_doctors = AvailableTime.objects.filter(available_date=date).values('doctor').distinct()
        doctors = User.objects.filter(Q(id__in=available_doctors))
        data = [{'doctor_id': doctor.id, 'name': doctor.name, 'department': doctor.department} for doctor in doctors]
        return JsonResponse({'doctors': data})
    else:
        return JsonResponse({'error': 'Invalid request'})



def fetch_time_list(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        date = request.POST.get('date')
        doctor_id = request.POST.get('doctor_id')

        if not date or not doctor_id:
            return JsonResponse({'data': 'not selected'})
        
        doctor_time = AvailableTime.objects.filter(doctor_id=doctor_id, available_date=date)
        data = [{'doctor_time': doctor.available_time} for doctor in doctor_time]
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error': 'Invalid request'})



def fetch_slot_list(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        date = request.POST.get('date')
        doctor_id = request.POST.get('doctor_id')
        time = request.POST.get('time')

        if not date or not doctor_id or not time:
            return JsonResponse({'data': 'not selected'})
        
        patient_tokens = PatientToken.objects.filter(doctor_id=doctor_id, date=date).values_list('token_no', flat=True)
        available_tokens = AvailableTime.objects.get(doctor_id=doctor_id, available_date=date, available_time=time).token_count
        available_tokens = [x for x in range(1, available_tokens+1)]
        available_tokens = list(set(available_tokens) - set(patient_tokens))

        if available_tokens == 0:
            return JsonResponse({"slots": None})
        return JsonResponse({"slots": available_tokens})
    else:
        return JsonResponse({'error': 'Invalid request'})
