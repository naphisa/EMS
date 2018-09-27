from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_bootstrap3_daterangepicker import fields,widgets
from django.contrib.admin.widgets import AdminDateWidget
from .models import CalcSalary, Documents, Leaves, Records
import datetime
from django.forms.extras.widgets import SelectDateWidget
from django.forms import extras

class UserForm(UserCreationForm):
    username = forms.EmailField(label='Email', required=True)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
class RegisterForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1920, 2020)))
    date_of_employment = forms.DateField(widget=forms.SelectDateWidget(years=range(1920, 2020)))
    class Meta:
        model = Records
        fields = ['profilepic', 'firstname', 'surname', 'othername', 'gender', 'address', 'email', 'date_of_birth', 'date_of_employment', 'position', 'department', 'appointment_type']

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.EmailField(label='Email')
    class Meta:
        model = User
        fields = ['username', 'password']

class LeaveForm(forms.ModelForm):
    start_date = forms.DateField(widget=SelectDateWidget)
    end_date = forms.DateField(widget=SelectDateWidget)
    class Meta:
         model = Leaves
         fields = ['leave_type', 'num_days', 'start_date', 'end_date' ]
class PaymentForm(forms.ModelForm):
    class Meta:
        model = CalcSalary
        fields = ['email', 'basic_salary', 'tax', 'nhis_charge', ]

class DocumentForm(forms.ModelForm):
    document_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Documents
        fields = ['email', 'document', 'document_file', ]