from django.shortcuts import render
from .models import *
import sweetify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
import random
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request,"index.html")

def register(request):
    if request.POST:
        try:
            user=User.objects.get(email=request.POST['email'])
            sweetify.error(request,"Email Already Exists")
            return render(request,"register.html")
        except:
            if request.POST['password'] == request.POST['password2']:
                user=User.objects.create(
                    email=request.POST['email'],
                    password=request.POST['password'],
                )
                sweetify.success(request,"Ragistration Succssesfully")
                return render(request,"login.html")
            else:
                sweetify.info(request,"Password Does Not Match")
                return render(request,"register.html")
    else:
        return render(request,"register.html")
    
def login(request):
    if request.POST:
        try:
            user=User.objects.get(email=request.POST['email'])
            print("================",user.email)
            if user.password==request.POST['password']:
                print("========>>>>>>>")
                request.session['email']=user.email
                print("--------------------------")
                sweetify.success(request,"Login Successfully")
                return render(request,"index.html")
            else:
                sweetify.error(request,"Password Does Not Match")
                return render(request,"login.html")
        except:
            sweetify.error(request,"Email Does Not Exists??")
            return render(request,"login.html")
    else:
        return render(request,"login.html")
    
def logout(request):
    del request.session['email']
    sweetify.success(request,"Logout Successfully")
    return render(request,"login.html")

def forgot_password(request):
    if request.POST:
        try:
            user=User.objects.get(email=request.POST['email'])
            print("================",user)
            email = request.POST['email']
            request.session['email']=email
            print(email)
            otp=random.randint(1001,9999)
            request.session['otp']=otp
            print(otp)
            mymailfunction("Welcome to Forget Password","email_template",email,{'email':email,"otp":otp})
            sweetify.success(request,"OTP Sent Successfully")
            return render(request,"email_otp.html")
        except:
            print("######################")
            sweetify.info(request,"Email Not Exists")
            return render(request,"forgot-password.html")
    else:
        return render(request,"forgot-password.html")

def mymailfunction(subject,template,to,context):
    template_str = template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'kurmipurshottam@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def email_otp(request):
    if request.POST:
        otp=int(request.session['otp'])
        uotp=int(request.POST['otp'])
        print(otp)
        print(uotp)
        if otp==uotp:
            print("hello")
            del request.session['otp']
            return render(request,"email_reset.html")
        else:
            msg="Invalid OTP"
            sweetify.error(request,msg)
            return render(request,"otp.html")
    else:
        return render(request,"otp.html")

def email_reset(request):
     if request.POST:
            user= User.objects.get(email=request.session['email'])
            if request.POST['npassword']==request.POST['ncpassword']:
                user.password=request.POST['ncpassword']
                user.save()
                msg="password reset successfuly" 
                sweetify.success(request,msg)
                del request.session['email']
                return render(request,"login.html")
               
            else:
                msg="New Password and Confirm New Password Does Not Match" 
                sweetify.error(request,msg)
                return render(request,"email_reset.html")        
     else:
          return render(request,"email_reset.html") 

def employees_list(request):
        employee=Employees.objects.all()
        print(employee)
        if request.POST:
            if request.POST['password']==request.POST['password2']:
                employees = Employees.objects.create(
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    username = request.POST['username'],
                    email = request.POST['email'],
                    password = request.POST['password'],
                    joining_date = datetime.strptime(request.POST['joining_date'], '%d/%m/%Y').strftime('%Y-%m-%d'),
                    employee_id = request.POST['employee_id'],
                    phone = request.POST['phone'],
                    company = request.POST['company'],
                    department = request.POST['department'],
                    designation = request.POST['designation'],
                )
                sweetify.success(request,"Employee Add Successfully..")
                return render(request,"employees-list.html",{'employee':employee})
            else:
                sweetify.warning(request,"password and Conifrm pass can not match")
                return render(request,"employees-list.html",{'employee':employee})
        else:
            return render(request,"employees-list.html",{'employee':employee})