# Generated by Django 5.0.6 on 2024-07-06 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS_APP', '0004_alter_employees_joining_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='joining_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
