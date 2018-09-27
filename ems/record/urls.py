from django.conf.urls import url
from . import views

app_name = 'record'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', views.UserProfile.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/leave/$', views.leave_view, name='leave'),
    url(r'^login/account/$', views.account_view, name='account'),
    url(r'^login/leavehist/$', views.leavehist_view, name='leavehist'),
    url(r'^registerpay/$', views.register_pay, name='registerpay'),
    url(r'^registerrecord/$', views.RegisterFormView.as_view(), name='registerrecord'),
    url(r'^login/payment/$', views.payment_view, name='payment'),
    url(r'^login/admin/totalpay/$', views.total_salary, name='totalpay'),
    url(r'^registerrecord/upload/$', views.uploadformview, name='upload'),
    #url(r'^login/$', views.login_view, name='login'),
    #url(r'^register/$', views.login_view, name='register'),
    #url(r'^emplist/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^emplist/$', views.EmpList.as_view(), name='emps'),

]