from django.contrib import admin
from django.urls import path
from testapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_req,  name='login'),
    path('create-sales/', views.create_sales,  name='sales'),
    
    path('signup/', views.signup,  name='signup'),
    path('fetchitems/', views.fetchitems,  name='fetchitems'),
    path('my-order/', views.myorder,  name='myorder'),
    path('view-order/<int:pk>', views.vieworder,  name='vieworder'),
    path('followup/<int:pk>', views.followup,  name='followup'),
    path('managefollowup/', views.managefollowup,  name='managefollowup'),
    path('generate-invoice/<int:pk>', views.generateinvoice,  name='generateinvoice'),
    path('logout/', views.logout_view, name ="logout"),
]
