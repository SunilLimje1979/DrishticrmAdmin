from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('hello/',hello,name='hello'),
    path('login/',Login,name='login'),
    path('base/',base,name='base'),
    path('index/',index,name='index'),
    path('Logout/',Logout,name='Logout'),
    path('allRegistered/',allRegistered,name='allRegistered'),
    path('get_appmaster_details/<int:id>',get_appmaster_details,name='get_appmaster_details'),
    path('filter_doctors/',filter_doctors, name='filter_doctors'),
    path('reset_password/',reset_password,name='reset_password'),
    path('toggle_subscription_status/',toggle_subscription_status,name='toggle_subscription_status'),

]
