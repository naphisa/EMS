from django.conf.urls import url
from . import views

app_name = 'records'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', views.UserProfile.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/leave/$', views.leave_view, name='leave'),
    #url(r'^login/$', views.login_view, name='login'),
    #url(r'^register/$', views.login_view, name='register'),
    #url(r'^emplist/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^emplist/$', views.EmpList.as_view(), name='emps'),

]