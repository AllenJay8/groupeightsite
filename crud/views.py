from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Genders

def gender_list(request):
    genders = Genders.objects.all()
    return render(request, 'gender/GendersList.html', {'genders': genders})

def add_gender(request):
    if request.method == 'POST':
        gender_name = request.POST.get('gender')
        if gender_name:
            Genders.objects.create(gender=gender_name)
            messages.success(request, 'Gender added successfully!')
            return redirect('gender_list')
    return render(request, 'gender/AddGender.html')

def edit_gender(request, id):
    gender = get_object_or_404(Genders, id=id)
    if request.method == 'POST':
        gender_name = request.POST.get('gender')
        if gender_name:
            gender.gender = gender_name
            gender.save()
            messages.success(request, 'Gender updated successfully!')
            return redirect('gender_list')
    return render(request, 'gender/EditGender.html', {'gender': gender})

def delete_gender(request, id):
    gender = get_object_or_404(Genders, id=id)
    gender.delete()
    messages.success(request, 'Gender deleted successfully!')
    return redirect('gender_list')