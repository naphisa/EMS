from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_bootstrap3_daterangepicker import fields,widgets
from django.contrib.admin.widgets import AdminDateWidget
from .models import Leave
import datetime
from django.forms.extras.widgets import SelectDateWidget

class UserForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    #password = forms.CharField(label='Password', widget=forms.PasswordInput)
    #password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']

class LeaveForm(forms.ModelForm):
    start_date = forms.DateField(widget=SelectDateWidget)
    end_date = forms.DateField(widget=SelectDateWidget)
    class Meta:
         model = Leave
         fields = ['leave_type', 'num_days', 'start_date', 'end_date', ]