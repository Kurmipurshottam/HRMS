from django.shortcuts import render,get_object_or_404,redirect
from .models import *
import sweetify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
import random
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.

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
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Received POST request with username:", username)
        print("Received POST request with password:", password)

        # First try to authenticate with Employees model
        try:
            emp = Employees.objects.get(username=username)
            print("Employee found:", emp)
            if emp.password == password:
                print("Password matches for employee.")
                request.session['username'] = emp.username
                sweetify.success(request, "Login Successfully")
                return render(request, "employee_dashboard.html")
            else:
                print("Password does not match for employee.")
                sweetify.error(request, "Password Does Not Match")
                return render(request, "login.html")
        except Employees.DoesNotExist:
            print("Employee does not exist.")
            sweetify.error(request, "Email Does Not Exist")

        # Fall back to Django's built-in authentication
        user = authenticate(request, username=username, password=password)
        print("================>",user)
        if user is not None:
            print("User authenticated successfully.")
            auth_login(request, user) 
            request.session['username'] = username
            sweetify.success(request, "Login Successfully")
            return redirect('admin_dashboard')
        else:
            print("Django authentication failed.")
            sweetify.error(request, "Password Does Not Match")
            return render(request, 'login.html', {'error': 'Invalid Username and Password'})
    else:
        print("Rendering login page.")
        return render(request, 'login.html')


def forgot_password(request):
    if request.POST:
        try:
            employees=Employees.objects.get(email=request.POST['email'])
            print("================",employees)
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
            employees= Employees.objects.get(email=request.session['email'])
            if request.POST['npassword']==request.POST['ncpassword']:
                employees.password=request.POST['ncpassword']
                employees.save()
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

def logout(request):
    try:
        print("Attempting to delete username from session...")
        del request.session['username']
        sweetify.success(request, "Logout Successfully")
        return render(request, "login.html")
    except KeyError:
        print("Username not found in session.")
    
    print("Logging out user using Django's auth_logout...")
    auth_logout(request)
    sweetify.success(request, "Logout Successfully")
    return render(request, "login.html")


def admin_dashboard(request):
    emp = Employees.objects.count()
    context={
        'emp':emp
    }
    
    return render(request,"admin_dashboard.html",context)

def profile(request):
    return render(request,"profile.html")

def employee_dashboard(reuqest):
    return render(reuqest,"employee_dashboard.html")

def employees_list(request):
    employees = Employees.objects.all()
    departments = Department.objects.all()
    designations = Designation.objects.all()
    
    if request.method == "POST":
        if request.POST['password'] == request.POST['password2']:
            Employees.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'],
                joining_date=datetime.strptime(request.POST['joining_date'], '%d/%m/%Y').strftime('%Y-%m-%d'),
                employee_id=request.POST['employee_id'],
                phone=request.POST['phone'],
                company=request.POST['company'],
                department=Department.objects.get(id=request.POST['department']),
                designation=Designation.objects.get(id=request.POST['designation']),
            )
            sweetify.success(request, "Employee Add Successfully..")
            return render(request, 'employees-list.html', {'employees': employees, 'departments': departments, 'designations': designations})
        else:
            sweetify.warning(request, "Password and Confirm password do not match")
            return render(request, 'employees-list.html', {'employees': employees, 'departments': departments, 'designations': designations})
    else:
        return render(request, 'employees-list.html', {'employees': employees, 'departments': departments, 'designations': designations})
        
def employees_serch(request):
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    designation_id = request.GET.get('designation')
    print("================================",designation_id)
    employee = Employees.objects.all()
    departments = Department.objects.all()
    designations = Designation.objects.all()

    if employee_id:
        employees = employee.filter(employee_id__icontains=employee_id)
    
    if employee_name:
        employees = employee.filter(
            Q(first_name__icontains=employee_name) | Q(last_name__icontains=employee_name)
        )

    if designation_id:
        employees = employee.filter(designation_id=designation_id)

    context = {
        'employees': employees,
        'departments': departments,
        'designations': designations,
    }
    return render(request, 'employees-list.html',context)

def update_employee(request,id):
    employees = Employees.objects.all()
    departments = Department.objects.all()
    designations = Designation.objects.all()
    employee = get_object_or_404(Employees, pk=id)
    if request.method == 'POST':
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.email = request.POST.get('email')
        department_id = request.POST.get('department')
        designation_id = request.POST.get('designation')
        employee.department = Department.objects.get(id=department_id)
        employee.designation = Designation.objects.get(id=designation_id)
        employee.save()
        sweetify.success(request, "Employee Updated Successfully")
        return render(request, 'employees-list.html', {'employees': employees, 'departments': departments, 'designations': designations})
    return render(request, 'employees-list.html', {'employees': employees, 'departments': departments, 'designations': designations})

def delete_employee(request,id):
    employees=Employees.objects.all()
    print(employees)
    employee = get_object_or_404(Employees, id=id)
    print(employee)
    employee.delete()
    sweetify.success(request,"employee deleted successfully")
    return render(request,"employees-list.html",{'employees':employees})

def departments(request):
    department = Department.objects.all()
    if request.POST:
        Department.objects.create(
            department = request.POST['department']
        )
        sweetify.success(request,"Departments Add Successfully..")
        return render(request,"departments.html",{'department':department})
    else:
        return render(request,"departments.html",{'department':department})
    

def departments_delete(request,id):
    department = Department.objects.all()
    departments = get_object_or_404(Department, id=id)
    departments.delete()
    sweetify.success(request,"Departments Delete Successfully..")
    return render(request,"departments.html",{'department':department})  
    

def departments_update(request,id):
    departments = get_object_or_404(Department, id=id)
    if request.method == 'POST':
        department_name = request.POST['department']
        departments.department = department_name
        departments.save()
        department = Department.objects.all()
        sweetify.success(request, "Department updated successfully.")
        return render(request, 'departments.html',{'department':department}) 
    return render(request, 'departments.html',{'department':department}) 

def designations(request):
    designation = Designation.objects.all()
    departments = Department.objects.all()
    
    if request.method == "POST":
        designations = request.POST.get('designation')  
        department_id = request.POST.get('department')  
        
        department = Department.objects.get(id=department_id)
        
        Designation.objects.create(
            designation=designations,
            department=department
        )       
        sweetify.success(request, "Designation Added Successfully..")
        return render(request, "designations.html", {'designation': designation, 'departments': departments}) 
    return render(request, "designations.html", {'designation': designation, 'departments': departments})

def designations_update(request, id):
    designations = get_object_or_404(Designation, pk=id)
    if request.method == 'POST':
        designation = request.POST.get('designation')
        department_id = request.POST.get('department')
        department = Department.objects.get(id=department_id)
        
        designations.designation = designation
        designations.department = department
        designations.save()
        designation = Designation.objects.all()
        sweetify.success(request, "Designation updated successfully.")
        return render(request, 'designations.html',{'designation':designation})
    return render(request, 'designations.html',{'designation':designation})

    
def designations_delete(request, id):
    designation = Designation.objects.all()
    designations = get_object_or_404(Designation, id=id)
    designations.delete()
    
    sweetify.success(request, "Designation deleted successfully.")
    return render(request, 'designations.html',{'designation':designation})

def holidays(request):
    if request.POST:
        
    return render(request,"holidays.html")