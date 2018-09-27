# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout,user_logged_in
from django.views.generic import View
from django.views import generic
from django.http import HttpResponse,request
from .models import Records, CalcSalary, Leaves, CompanyInfo
from .forms import UserForm, LoginForm, LeaveForm, PaymentForm, RegisterForm, DocumentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)

# Create your views here.
def index(request):
    return render(request, 'record/index.html')

class EmpList(generic.ListView):
    template_name = 'record/emplist.html'
    def get_queryset(self):
        return Records.objects.all()
           # email = form.cleaned_data['email']
        #password = form.cleaned_data['password']

        #render(request, "login.html", {form: form})

class RegisterFormView(LoginRequiredMixin, View):
    form_class = RegisterForm
    template_name = 'record/register_form.html'
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)
        profilepic = form['profilepic'].data
        firstname = form['firstname'].data
        surname = form['surname'].data
        othername = form['othername'].data
        gender = form['gender'].data
        address = form['address'].data
        email = form['email'].data
        date_of_birth = form['date_of_birth'].data
        date_of_employment = form['date_of_employment'].data
        position = form['position'].data
        department = form['department'].data
        appointment_type = form['appointment_type'].data
        print(address)
        if form.is_valid():
            Records.objects.create(profilepic=profilepic, firstname=firstname,surname=surname,othername=othername,gender=gender,
                                   address=address,email=email,date_of_birth=date_of_birth,date_of_employment=date_of_employment,position=position,department=department,appointment_type=appointment_type)
            return redirect('record:upload')
@login_required
def uploadformview(request):
    form_class = DocumentForm
    if request.method == 'GET':
        form = form_class(None)
        return render(request, 'record/upload_form.html', {'form': form})
    elif request.method == 'POST':
        form = form_class(request.POST)
        email = form['email'].data
        document = form['document'].data
        document_file = form['document_file'].data
        user = Records.objects.get(email=email)
        user.documents_set.create(staff=user,email=email, document=document, document_file=document_file)
        return redirect('record:upload')
class UserFormView(View):
    form_class = UserForm
    template_name = 'record/registration_form.html'
    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #process input data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            #cleaned/normalized data
            #username = form.cleaned_data['username']
            #password1 = form.cleaned_data['password']
            #password2 = form.cleaned_data['password2']
            return HttpResponse('user registered!!!')
        return HttpResponse('user not registered!!!')

class UserProfile(View):
    form_class = LoginForm
    template_name = 'record/profile.html'
    def get(self, request):
        form = self.form_class(None)
        return render(request, 'record/login_form.html', {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid:
            username = form['username'].data
            password = form['password'].data
            user = authenticate(username=username, password=password)
            #user1 = User.objects.get(username=username)
            #print(user1)
            #st = get_current_user()
            if user is not None:
                if request.user.is_superuser:
                    login(request, user)
                    return render(request, 'record/admin_page.html')
                    # total_pay = 0
                    # staffs = CalcSalary.objects.all()
                    # for staff in staffs:
                    #     total_pay += staff.net_pay
                    # return render(request, 'record/payment.html', {'total_pay': total_pay})
                   # obj = CompanyMoneyRecords.objects.all()
                   # return render(request, 'records/admin_page', {'obj': obj})
                else:
                    obj = Records.objects.get(email=username)
                    if obj is None:
                        return('Staff is not registered!!')
                    else:
                        request.session['username'] = username
                        login(request, user)
                        return render(request, self.template_name, {'obj': obj})
            return HttpResponse('user doesnt exist!!')
        return HttpResponse('form invalid')
@login_required
def leave_view(request):
    form_class = LeaveForm
    template_name = 'record/leave_form.html'
    if request.method == 'GET':
        print(request.user)
        form = form_class(None)
        return render(request, template_name, {'form': form})
    elif request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            #staff = request.user
            #leave_type = form.cleaned_data['leave_type']
            leave_type = form['leave_type'].data
            print(leave_type)
            num_days = form['num_days'].data
            start_date = form['start_date'].data
            end_date = form['end_date'].data
            cur_user = request.user
            user = Records.objects.get(email=cur_user)
            user.leaves_set.create(staff=user, leave_type=leave_type, num_days=num_days, start_date=start_date, end_date=end_date)
            #form.save(commit=True)
            return HttpResponse('Applied successfully')
            #form.staff = User.objects.get(username=request.user)
            #form.save()
@login_required
def register_pay(request):
    form_class = PaymentForm
    template_name = 'record/calcsalary_form.html'
    if request.method == 'GET':
        form = form_class(None)
        return render(request, template_name, {'form': form})
    elif request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            staff = Records.objects.get(email=email)
            basic_salary = form['basic_salary'].data
            tax = form['tax'].data
            nhis_charge = form['nhis_charge'].data
            net_pay = CalcSalary.calc_salary(basic_salary=basic_salary, tax=tax, nhis_charge=nhis_charge)
            print(net_pay)
            staff.calcsalary_set.create(staff=staff, email=email, basic_salary=basic_salary, tax=tax, nhis_charge=nhis_charge, net_pay=net_pay)
            CompanyInfo.cummulate_salary(basic_salary=basic_salary)
            return render(request, 'record/admin_page.html')
@login_required
def payment_view(request):
    cur_user = request.user
    user = Records.objects.get(email=cur_user)
    payment_details = user.calcsalary_set.get(email=cur_user)
    return render(request, 'record/payment.html', {'payment_details': payment_details})
@login_required
def total_salary(request):
    obj = CompanyInfo.objects.get(pk=1)
    print(obj)
    return render(request, 'record/total_payment.html', {'obj': obj})
    # total_pay = 0
    # staffs = CalcSalary.objects.all()
    # for staff in staffs:
    #     total_pay += staff.net_pay



@login_required
def leavehist_view(request):
    cur_user = request.user
    obj = Records.objects.get(email=cur_user)
    #leav  = obj.leaves_set.all()
    return render(request, 'record/leave_hist.html', {'obj': obj})


@login_required
def account_view(request):
    cur_user = request.user
    obj = Records.objects.get(email=cur_user)
    return render(request, 'record/profile.html', {'obj': obj})

@login_required
def logout_view(request):
    try:
        logout(request)
        #del request.session['username']
        return redirect('record:index')
    except KeyError:
        pass
    return HttpResponse('You are logged out!!!')

