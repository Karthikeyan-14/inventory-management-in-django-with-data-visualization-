"""
URL configuration for inv_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   
    path('',views.start,name="go-start"),
    path('login',views.log,name='go_log'),
    path('register',views.reg,name='go_reg'),
    path('otp',views.temp_otp,),
    path('otp_check',views.otp_chk,),
    path('otp_resend',views.resend,name="resend"),

    path('client_log',views.log_in),
    path('saved',views.save_data,name='save_query'),
    path('modal',views.modal,name='modal_view'),
    path('response',views.responses,name='response_data'),
    path('modall',views.modal2,name='modal2_view'),
    
    path('reports',views.report_data,name='report'),

    
    path('responded',views.fetch_res,name='respond_to'),
    path('status',views.update,name='update_status'),
    path('getque',views.get_question,name='get_ques'),
    path('save',views.save_res,name='save_response'),
    path('admin_response',views.response_admin,name='response__admin_data'),

    path('small_ad',views.go_small,name="go-end"),





    path('task', views.task_board, name='task_board'),
    path('add/<str:category>/', views.add_task, name='add_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update_category/<int:task_id>/', views.update_category, name='update_category'),


    path('', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('get-task-data/', views.get_task_data, name='get_task_data'),
    path('get-task-details/', views.get_task_details, name='get_task_details'),
    path('delete-closed-tasks/', views.delete_closed_tasks, name='delete_closed_tasks'),
    path('generate-report/', views.generate_report, name='generate_report'),
]


 
    

