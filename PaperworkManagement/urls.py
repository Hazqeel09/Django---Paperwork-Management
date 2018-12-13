'''
Created on 11 Oct 2018

@author: Hazqeel
'''

from django.urls import path
from . import views

app_name = 'PaperworkManagement'
urlpatterns = [
    path('',views.index, name = 'index'),
    #login
    path('login/', views.login, name = 'login'),
    path('login/auth', views.auth_user, name = 'auth_user'),
    #signup
    path('signup/', views.signup, name = 'signup'),
    path('signup/admin', views.signup_admin, name = 'signup_admin'),
    path('signup/org', views.signup_org, name = 'signup_org'),
    #signup process
    path('signup/process', views.signup_process, name = 'signup_process'),
    path('signup/process/admin', views.process_admin, name = 'process_admin'),
    path('signup/process/org', views.process_org, name = 'process_org'),
    #logout
    path('logged_out/', views.logout, name = 'logout'),
    #user view
    path('user/upcoming_event', views.upcoming, name = 'upcoming'),
    #organization view
    path('organization/',views.view_org, name = 'view_org'),
    path('<str:ppwcode>/dlppw/',views.dlppw, name = 'dlppw'),
    path('organization/budget_flow/',views.budget_flow, name = 'budget_flow'),
    #write paperwork
    path('view_ppw/', views.view_ppw, name = 'view_ppw'),
    path('view_ppw/write_ppw/', views.write_ppw, name = 'write_ppw'),
    path('view_ppw/process_ppw/', views.process_ppw, name = 'process_ppw'),
    path('view_ppw/update_ppw/<str:ppwcode>/', views.update_ppw, name = 'update_ppw'),
    path('view_ppw/delete_ppw/<str:ppwcode>/', views.delete_ppw, name = 'delete_ppw'),
    path('view_ppw/done_ppw/', views.done_ppw, name = 'done_ppw'),
    ]