# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.extras.widgets import SelectDateWidget
from crum import get_current_user

# Create your models here.
class Record(models.Model):
    Gender = (('M', 'Male'), ('F', 'Female'))
    profilepic = models.FileField(default='/static/images/default')
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    othername = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=Gender)
    address = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    DOB = models.DateField()
    DOE = models.DateField()
    department = models.CharField(max_length=100)
    appointment_type = models.CharField(max_length=100)
    document = models.FileField()
    def get_absolute_url(self):
        return reverse('records:profile', kwargs={'pk': self.pk})
    def __str__(self):
        return self.firstname +'-'+ self.surname

class Leave(models.Model):
    Status = (('1', 'Pending'), ('2', 'Approved'), ('3', 'Declined'))
    Leave_Types = (('1', 'Annual'), ('2', 'Sick'), ('3', 'Emergency'), ('4', 'Casual'))
    leave_type = models.CharField(max_length=1, choices=Leave_Types)
    num_days = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=1, choices=Status, default='1')
    #settings.AUTH_USER_MODEL, default=1



