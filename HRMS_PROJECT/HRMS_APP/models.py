from django.db import models

# Create your models here.
class User(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.email

class Employees(models.Model):
    company=(
        ("Delta","Delta"),
        ("Infotech","Infotech"),
        ("TCS","TCS"),
        
    )

    department=(
        ("Web Development","Web Development"),
        ("Marketing","Marketing"),
        ("Backend Development","Backend Development"),
        ("Frontend Development","Frontend Development"),
    )

    designation=(
        ("Web Designer","Web Designer"),
        ("Web Developer","Web Developer"),
        ("Android Developer","Android Developer"),
        ("Backend Developer","Backend Developer")
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
    department = models.CharField(max_length=20,choices=department)
    designation = models.CharField(max_length=20,choices=designation)

    def __str__(self):
        return self.first_name + " || " + self.last_name