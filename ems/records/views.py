# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout,user_logged_in
from django.views.generic import View
from django.views import generic
from django.http import HttpResponse,request
from .models import Record
from .forms import UserForm, LoginForm, LeaveForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'records/index.html')

class EmpList(generic.ListView):
    template_name = 'records/emplist.html'
    def get_queryset(self):
        return Record.objects.all()
           # email = form.cleaned_data['email']
        #password = form.cleaned_data['password']

        #render(request, "login.html", {form: form})

class UserFormView(View):
    form_class = UserForm
    template_name = 'records/registration_form.html'
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
            #obj = User.objects.get(username=username)
            #print(obj)
            # if password1 == password2:
            #     user.set_password(password1)
            #     user.save()
            #     return HttpResponse('user registered!!!')
            # elif password1 != password2:
            return HttpResponse('user registered!!!')
        return HttpResponse('user not registered!!!')
class UserProfile(View):
    form_class = LoginForm
    template_name = 'records/profile.html'
    def get(self, request):
        form = self.form_class(None)
        return render(request, 'records/login_form.html', {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)
        #user = form.save(commit=False)
        if form.is_valid:
            username = form['username'].data
            password = form['password'].data
            user = authenticate(username=username, password=password)
            #user1 = User.objects.get(username=username)
            #print(user1)
            if user is not None:
                print(user)
                obj = Record.objects.get(email=username)
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
    template_name = 'records/leave_form.html'
    if request.method == 'GET':
        print(request.user)
        form = form_class(None)
        return render(request, template_name, {'form': form})
    elif request.method == 'POST':
        form = form_class(request.POST)
        date = form['start_date'].data
        print(date)
        if form.is_valid():
            form.save(commit=True)
            print(form['staff'])
            return HttpResponse('Applied successfully')
            #form.staff = User.objects.get(username=request.user)
            #form.save()
        return redirect('records:login')


@login_required
def logout_view(request):
    try:
        logout(request)
        #del request.session['username']
        return redirect('records:index')
    except KeyError:
        pass
    return HttpResponse('You are logged out!!!')

