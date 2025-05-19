from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password

# Create your views here.

def gender_list(request):
    try:
        genders = Genders.objects.all() # SELECT * FROM tbl_genders;

        data = {
            'genders':genders
        }

        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during load genders: {e}')

def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')
            
            Genders.objects.create(gender=gender).save() # INSERT INTO tbl_genders (gender) VALUES ('gender');
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list/')
        else:
            return render(request, 'gender/AddGender.html')
    except Exception as e:
       return HttpResponse(f'Error occured during add gender: {e}')

def edit_gender(request, genderId):
    try:
        genderObj = Genders.objects.get(pk=genderId)

        if request.method == 'POST':
            gender = request.POST.get('gender')

            genderObj.gender = gender
            genderObj.save()

            messages.success(request, 'Gender updated successfully!')
            return redirect('/gender/list/')  # Redirect after success

        data = {
            'gender': genderObj
        }
        return render(request, 'gender/EditGender.html', data)
        
    except Exception as e:
        return HttpResponse(f'Error occurred during edit gender: {e}')

def delete_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId) # SELECT * FROM tbl_genders WHERE id = genderId;
            genderObj.delete() # DELETE FROM tbl_genders WHERE id = genderId;

            messages.success(request, 'Gender deleted successfully!')
            return redirect('/gender/list/')
        else:
            genderObj = Genders.objects.get(pk=genderId) # SELECT * FROM tbl_genders WHERE id = genderId;

            data = {
                'gender': genderObj
            }
    
            return render(request, 'gender/DeleteGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during delete gender: {e}')

def user_list(request):
    try:
        userObj = Users.objects.select_related('gender') # SELECT * FROM tbl_users INNER JOIN tbl_genders ON tbl_users.gender_id = tbl_genders.id;
    
        data = {
           'users': userObj,
         }

        return render(request, 'user/UsersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during load users: {e}')

def add_user(request):
    try:
        genderObj = Genders.objects.all()  

        if request.method == 'POST':
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')

            
            form_data = {
                'full_name': fullName,
                'gender': gender,
                'birth_date': birthDate,
                'address': address,
                'contact_number': contactNumber,
                'email': email,
                'username': username,
            }

            
            if not all([fullName, gender, birthDate, address, contactNumber, username, password, confirmPassword]):
                messages.error(request, 'All required fields must be filled.')
            elif password != confirmPassword:
                messages.error(request, 'Password and Confirm Password do not match!')
            elif Users.objects.filter(username=username).exists():
                 messages.error(request, 'Username already exists!')
                 
            else:
                Users.objects.create(
                    full_name=fullName,
                    gender=Genders.objects.get(pk=gender),
                    birth_date=birthDate,
                    address=address,
                    contact_number=contactNumber,
                    email=email,
                    username=username,
                    password=make_password(password)
                )
                messages.success(request, 'User added successfully!')
                return redirect('/user/add/')

           
            return render(request, 'user/AddUser.html', {
                'genders': genderObj,
                'form_data': form_data
            })

        else:
            return render(request, 'user/AddUser.html', {
                'genders': genderObj
            })

    except Exception as e:
        return HttpResponse(f'Error occurred during add user: {e}')
    
def edit_user(request, userId):
    try:
        user = Users.objects.get(pk=userId)
        genders = Genders.objects.all()

        if request.method == 'POST':
            user.full_name = request.POST.get('full_name')
            user.gender = Genders.objects.get(pk=request.POST.get('gender'))
            user.birth_date = request.POST.get('birth_date')
            user.address = request.POST.get('address')
            user.contact_number = request.POST.get('contact_number')
            user.email = request.POST.get('email')
            user.username = request.POST.get('username')

            user.save()
            messages.success(request, 'User updated successfully!')
            return redirect('/user/list/')
        
        data = {
            'user': user,
            'genders': genders,
            'form_data': request.POST
        }
        return render(request, 'user/EditUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during edit user: {e}')


def delete_user(request, userId):
    try:
        user = Users.objects.get(pk=userId)

        if request.method == 'POST':
            user.delete()
            messages.success(request, 'User deleted successfully!')
            return redirect('/user/list/')

        return render(request, 'user/DeleteUser.html', {'user': user})
    except Exception as e:
        return HttpResponse(f'Error occurred during delete user: {e}')
    

    