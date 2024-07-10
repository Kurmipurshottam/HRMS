"""
URL configuration for HRMS_PROJECT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home')
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('email_otp', views.email_otp, name='email_otp'),
    path('email_reset', views.email_reset, name='email_reset'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('logout', views.logout, name='logout'),
    
    path('profile', views.profile, name='profile'),

    path('employee_dashboard', views.employee_dashboard, name='employee_dashboard'),
    path('employees_list', views.employees_list, name='employees_list'),
    path('employees_serch', views.employees_serch, name='employees_serch'),
    path('delete_employee/ <int:id>/', views.delete_employee, name='delete_employee'),
    path('update_employee/ <int:id>/', views.update_employee, name='update_employee'),

    path('departments', views.departments, name='departments'),
    path('departments_delete/ <int:id>/', views.departments_delete, name='departments_delete'),
    path('departments_update/ <int:id>', views.departments_update, name='departments_update'),

    path('designations', views.designations, name='designations'),
    path('designations_delete/ <int:id>/', views.designations_delete, name='designations_delete'),
    path('designations_update/ <int:id>', views.designations_update, name='designations_update'),

    path('holidays', views.holidays, name='holidays'),
    path('holidays_delete/ <int:id>/', views.holidays_delete, name='holidays_delete'),
    path('holidays_update/ <int:id>', views.holidays_update, name='holidays_update'),

    

]
