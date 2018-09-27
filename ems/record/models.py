# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.db import models
from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from djmoney.models.fields import MoneyField
# Create your models here.
class Records(models.Model):
    Gender = (('Male', 'Male'), ('Female', 'Female'))
    profilepic = models.FileField(default='/default')
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    othername = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=Gender)
    address = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    date_of_employment = models.DateField()
    position = models.CharField(max_length=100, default='position')
    department = models.CharField(max_length=100)
    appointment_type = models.CharField(max_length=100)
    def get_absolute_url(self):
        return reverse('records:profile', kwargs={'pk': self.pk})
    def __str__(self):
        return self.firstname +'-'+ self.surname

class Documents(models.Model):
    File_Name = (('cv', 'cv'), ('birth_certificate', 'birth_certificate'), ('ssce_certificate', 'ssce_certificate'), ('OND_certificate', 'OND_certificate'),('valid_ID_card', 'valid_ID_card'),
                 ('first_degree_certificate', 'first_degree_certificate'), ('NYSC_certificate', 'NYSC_certificate'), ('MSc_certificate', 'MSc_certificate'))
    staff = models.ForeignKey(Records)
    email = models.EmailField()
    document = models.CharField(null=True, max_length=50, choices=File_Name, default='select document to upload')
    document_file = models.FileField(null=True)
    def __str__(self):
        return self.email+'--'+self.document

class Leaves(models.Model):
    Status = (('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined'))
    Leave_Types = (('annual', 'Annual'), ('sick', 'Sick'), ('emergency', 'Emergency'), ('casual', 'Casual'))
    staff = models.ForeignKey(Records, default='')
    leave_type = models.CharField(max_length=20, choices=Leave_Types)
    num_days = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status, default='pending')
    def __str__(self):
        return self.staff
    #settings.AUTH_USER_MODEL, default=1

class CalcSalary(models.Model):
    staff = models.ForeignKey(Records)
    email = models.EmailField()
    basic_salary = models.IntegerField()
    tax = models.IntegerField(default=0)
    nhis_charge = models.IntegerField(default=0)
    net_pay = models.IntegerField(default=0)
    #date = models.DateField(auto_now=True)
    # def __init__(self, basic_salary, tax, nhis_charge, *args, **kwargs):
    #     models.Model.__init__(*args, **kwargs)
    #     #self.staff = staff
    #     self.basic_salary = basic_salary
    #     self.tax = tax
    #     self.nhis_charge = nhis_charge
    @classmethod
    def calc_salary(cls, basic_salary, tax, nhis_charge):
        tax_amount = (int(tax) * int(basic_salary)) / 100
        nhis_amount = (int(nhis_charge) * int(basic_salary)) / 100
        reduction = tax_amount + nhis_amount
        net_pay = int(basic_salary) - reduction
        return net_pay
    def __str__(self):
        return self.email

class CompanyInfo(models.Model):
    tax = models.IntegerField(default=2)
    nhis_charge = models.IntegerField(default=2)
    total_salary_monthly = models.IntegerField(default=0, null=True)
    #total_salary_yearly = models.CharField(max_length=14, null=True)
    no_of_staff = models.IntegerField(null=True)
    date = models.DateField(auto_now=True)

    @classmethod
    def cummulate_salary(cls, basic_salary):
        if CompanyInfo.objects.count() == 0:
            total_staff = Records.objects.count()
            #total_yearly = basic_salary * 12
            CompanyInfo.objects.create(no_of_staff=total_staff, total_salary_monthly=basic_salary)

        elif CompanyInfo.objects.count() > 0:
            total_staff = Records.objects.count()
            obj = CompanyInfo.objects.get(pk=1)
            obj.total_salary_monthly = int(obj.total_salary_monthly) + int(basic_salary)
            obj.no_of_staff = total_staff
            obj.save()
            # obj1 = CompanyInfo.objects.get(pk=1)
            # obj1.total_salary_yearly = obj1.total_salary_monthly * 12
            # obj1.save()
