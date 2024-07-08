from django.db import models

# Create your models here.
class User(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.email

class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.department

class Designation(models.Model):
    designation = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.designation


class Employees(models.Model):
    company=(
        ("Delta","Delta"),
        ("Infotech","Infotech"),
        ("TCS","TCS"),   
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    employee_id = models.CharField(max_length=50)
    joining_date = models.DateField(null=True,blank=True)
    phone = models.CharField(max_length=12)
    company = models.CharField(max_length=20,choices=company)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " || " + self.last_name
    

