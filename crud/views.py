from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders

#Create your views here.

def add_gender(request):
    try: 
        if request.method == 'POST':
         gender = request.POSTg.get('gender')

         Genders.objects.create(gender=gender).save()
         messages.success(request, 'Gender added succesfully!')
         return HttpResponse('Gender added successfully!')
        else:
            return render(request, 'gender/Addgender.html')
    except Exception as e:
        return HttpResponse(f'Error occured during add gender: {e}')
