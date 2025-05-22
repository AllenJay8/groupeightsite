from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.

@login_required
def gender_list(request):
    try:
        genders = Genders.objects.all() # SELECT * FROM tbl_genders;

        data = {
            'genders':genders
        }

        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during load genders: {e}')
    
@login_required
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

@login_required
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
    
@login_required
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

@login_required
def user_list(request):
    try:
        query = request.GET.get('q')  

        if query:
            userObj = Users.objects.select_related('gender').filter(full_name__icontains=query)
        else:
            userObj = Users.objects.select_related('gender')  

        data = {
            'users': userObj,
        }

        return render(request, 'user/UsersList.html', data)

    except Exception as e:
        return HttpResponse(f'Error occurred during load users: {e}')
    
@login_required
def ajax_user_search(request):
    query = request.GET.get('q', '')
    userObj = Users.objects.select_related('gender').filter(full_name__icontains=query) if query else Users.objects.select_related('gender')

    html = render_to_string('user/user_rows.html', {'users': userObj})
    return JsonResponse({'html': html})

@login_required
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
                
            elif len(confirmPassword) < 3:
                messages.error(request, "Password must be at least 3 characters.")
            
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
    

@login_required
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

@login_required
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
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')

        try:
            user = Users.objects.get(username=username)  
            if check_password(password, user.password):  
                request.session['user_id'] = user.user_id  
                messages.success(request, 'Login successful!')
                return redirect('/user/list/')  
            else:
                messages.error(request, 'Invalid password')  
        except Users.DoesNotExist:
            messages.error(request, 'User does not exist') 
        except Exception as e:
            messages.error(request, f'Error occurred during login: {e}')

@login_required
def edit_user_password(request, user_id):
    try:
        user = Users.objects.get(pk=user_id)
        
        if request.method == 'POST':
            current = request.POST.get('current_password')
            new1 = request.POST.get('new_password1')
            new2 = request.POST.get('new_password2')

            if not check_password(current, user.password):
                messages.error(request, "Current password is incorrect.")
            elif new1 != new2:
                messages.error(request, "New passwords do not match.")
            elif len(new1) < 3:
                messages.error(request, "Password must be at least 3 characters.")
            else:
                user.password = make_password(new1)
                user.save()
                messages.success(request, "Password updated successfully.")
                return redirect('user_list')

        return render(request, 'user/ChangePasswordUser.html', {'user': user})
    except Users.DoesNotExist:
        return HttpResponse("User not found.")


# add pagnition 10 user every page