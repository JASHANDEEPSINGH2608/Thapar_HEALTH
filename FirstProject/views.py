from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .helpers import send_forgot_password_mail
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from FirstProject.models import Appointment
from FirstProject.models import signup
from FirstProject.models import data
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Prescription

import uuid
# Create your views here.
# views.py
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Appointment

from django.db.models import Max,Q

from django.shortcuts import get_object_or_404

def home_view(request, *args, **kwargs):
    appointment_id = None
    if request.method == "POST":
        appointment_id = request.POST.get('appointment_id')
        appointment = Appointment.objects.get(id=appointment_id)
        prescription_file = request.FILES.get('prescription_file')
        prescription = Prescription(appointment=appointment, file=prescription_file)
        prescription.save()

        # Save the prescription file and associate it with the appointment
        
        # Fetch the appointments for the currently logged-in user

        # Pass the user's appointments to the template
        
        try:
            # Get the latest appointment for the current user
            latest_appointment = Appointment.objects.filter(user=request.user).latest('created_at')

            # Check if the latest appointment is not None before updating
            if latest_appointment:
                latest_appointment.is_canceled = True
                latest_appointment.delete()
                messages.success(request, 'Latest appointment canceled successfully!')
            else:
                messages.error(request, 'No appointments found for the user.')
        except Appointment.DoesNotExist:
            messages.error(request, 'No appointments found for the user.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

        return redirect('home')
    appointmentss = Appointment.objects.filter(user=request.user,is_canceled=False)
    prescriptions = Prescription.objects.filter(appointment__user=request.user)
    return render(request, 'home.html', {'user_appointments': appointmentss,'prescriptions':prescriptions,'appointment_id':appointment_id})
    
    

  
# def about_view(request,*args,**kwargs):
#     my_context={

#         "my_text":"this is about us",
#         "my_number":456,
#         "my_list": [123,3,321],
#         "my_html":"<h1>hello world</h1>"
#     }
#     return render(request,"about.html",my_context)

# def product_detail_view(request):
#     obj=Product.objects.get(id=1)
#     context={

#         'title':obj.title,
#         'description':obj.description
#     }
#     return render(request,"product/detail.html",context)

def login_view(request,*args,**kwargs):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have been logged in!")
            if user.email=="abc1234@gmail.com":
                return redirect('doctor_view')
            return redirect('home')
        else:
            messages.success(request,"There was an error while you were logging in ,Please try again")
            return redirect('login_view')
    return render(request,"login.html",{})
@login_required
def logout_view(request,*args,**kwargs):
     logout(request)
     messages.success(request,"You have been logged out successfully!")
     return redirect('login_view')

def signup_view(request,*args,**kwargs):
    if request.method=='POST':
        First_Name=request.POST['first-name']
        Last_Name=request.POST['last-name']
        Email=request.POST['e-mail']
        Password=request.POST['password']
        roll_no = request.POST.get('roll_no')
        
        
        user = User.objects.create_user(username=Email, email=Email, password=Password, first_name=First_Name, last_name=Last_Name)
        user.save()


        profile = signup.objects.create(user=user, roll_no=roll_no)
        profile.save()

        if user is not None:
            messages.success(request,"You have successfully signed up!")
            return redirect('login_view')
            
        
    return render(request,'signup.html')

def forgot_view(request,*args,**kwargs):
    try:
            print("Method:", request.method)
            all_emails = [user.email for user in User.objects.all()]
            print("All emails in database:", all_emails)

            if request.method=='POST':
                 email=request.POST.get('email')
                 print("Recievd email:",email)
                 if email not in all_emails:
                    messages.error(request, "write valid email address")
                    return redirect('forgot_view')


                 user_obj=User.objects.get(email=email)
                 token=str(uuid.uuid4())
                 
                 send_forgot_password_mail(user_obj,token)
                 messages.success(request,"OTP has been send to your given email address")
                 return redirect('forgot_view')
    except Exception as e:
        print(e) 
    return render(request,'forgot.html',{})

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
import uuid
from django.utils import timezone

def change_view(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')  # Use 'user_id' instead of 'user_id'
            token = request.POST.get('token')

            if user_id is None:
                messages.success(request, 'No user_id found')
                return redirect(reverse('change_view', args=[token]))

            if new_password != confirm_password:
                messages.success(request, 'Password not confirmed')
                return redirect(reverse('change_view', args=[token]))

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()

            # Update the forget_password_token to indicate that it has been used
            profile_obj.forget_password_token = None
            profile_obj.save()

            messages.success(request, 'Password changed successfully. You can now log in.')
            return redirect('login_view')

        context = {
            'user_id': profile_obj.user.id,
            'token': token
        }

    except Exception as e:
        print(e)

    return render(request, 'change.html', context)

@login_required
def appointment_view(request,*args,**kwargs):
  
    if request.method=="POST":
        
        desc=request.POST.get('desc')
        time_slot=request.POST.get('time_slot')
        issue=request.POST.get('issue')
        db=Appointment(desc=desc,time_slot=time_slot,issue=issue)
        db.save()
        
        appointment = Appointment.objects.create(
            user=request.user,
            desc=desc,
            time_slot=time_slot,
            issue=issue)



    return render(request,"appointment.html")


from .forms import dataForm
from .models import data
from .forms import dataForm
from django.shortcuts import render, redirect


def userprofile_view(request, *args, **kwargs):
    user_profile,created = data.objects.get_or_create(user=request.user)

    if request.method == "POST":

        form = dataForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('userprofile_view')
    else:
        form = dataForm(instance=user_profile)
    
    
   
    return render(request, 'user_profile.html', {'form': form, 'user_profile': user_profile})

@login_required
def doctor_view(request,*args,**kwargs):
    appointments = Appointment.objects.exclude(user=None).order_by('time_slot')
    if request.method=='POST':
        
        cancel=request.POST.getlist('cancel')
        Appointment.objects.filter(id__in=cancel).delete()
        
        return redirect('doctor_view')

    return render(request,"doctorview.html",{'appointments':appointments})

from django.shortcuts import render
import pyautogui as pgi
import webbrowser
import time

@login_required
def automate_google_meet(request):
    appointments=Appointment.objects.all()
    return render(request, 'meet.html',{'appointments':appointments})

# views.py
from django.shortcuts import render, redirect
from .models import Appointment
@login_required
def history_view(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Fetch the appointments for the currently logged-in user
        appointment = Appointment.objects.filter(user=request.user,is_canceled=False)

        # Pass the user's appointments to the template
        return render(request, 'history.html', {'user_appointments': appointment})
    else:
        # If the user is not authenticated, you might want to redirect them to the login page
        return redirect('login_view')  # Adjust 'login' to the actual URL or name of your login page


def prescription_upload(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment = Appointment.objects.get(id=appointment_id)

        prescription_file = request.FILES.get('prescription_file')

        print("Prescription file received:", prescription_file)  # Debug message

        if prescription_file:
            # Save the prescription file and associate it with the appointment
            prescription = Prescription(appointment=appointment, file=prescription_file)
            prescription.save()

            print("Prescription saved successfully!")  # Debug message
        else:
            print("No prescription file received.")  # Debug message

        # Redirect to the appointment list page or any other page
        return redirect('doctor_view')
    
    return render(request, 'doctorview.html')

# views.py

from django.shortcuts import render
from .models import Prescription

def prescription_list(request):
    user_prescriptions = Prescription.objects.filter(appointment__user=request.user)
    return render(request, 'home.html', {'prescriptions': user_prescriptions})


def patient_view(request):

    appointment = Appointment.objects.filter(is_canceled=False).order_by('time_slot')
    context={
        'user_appointments':appointment,
    }
    return render(request,"patient.html",context)