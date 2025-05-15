from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders

# Create your views here.

def gender_list(request):
    try:
        genders = Genders.objects.all() 

        data = {
            'genders': genders
        }
        return render(request, 'gender/GendersList.html')
    except Exception as e:
        return HttpResponse(f'Error occurred during load genders: {e}')

def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')
            Genders.objects.create(gender=gender)
            messages.success(request, 'Gender added successfully!')
            return redirect('/ gender/list')
        else:
            return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f'Error occurred during add gender: {e}')