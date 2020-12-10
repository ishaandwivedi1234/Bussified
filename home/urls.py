from django.contrib import admin
from django.urls import path
from home.models import Customer
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.register, name='register'),
    path('dashboard', views.userDashboard, name='dashboard'),
    path('operator/register', views.operatorRegister, name='registerOperator'),
    path('operator', views.operatorLogin, name='loginOperator'),
    path('operator/dashboard', views.operatorDashboard, name='operatorDashboard'),
    path('operator/add/<int:operatorId>', views.addBus, name='addBus'),
    path('operator/logout', views.operatorLogout, name='operatorLogout'),
    path('logout', views.customerLogout, name='customerLogout'),
    path('book/<str:customerId>/<str:busId>/<str:date>',
         views.bookTickets, name='book'),
    path('dashboard/mybookings/<str:customerId>',
         views.myBookings, name='myBookings'),
    path('dashboard/mybookings/<str:customerId>/completed',
         views.filterCompleted, name='filterCompleted'),
    path('dashboard/mybookings/<str:customerId>/cancelled',
         views.filterCancelled, name='filterCancelled'),
    path('dashboard/mybookings/<str:customerId>/booked',
         views.filterBooked, name='filterbooked'),
    path('dashboard/mybookings/<str:customerId>/cancel/<str:ticketId>',
         views.cancelTicket, name='cancelTicket'),

    path('dashboard/account/<str:customerId>',
         views.userAccount, name='userAccount'),

    path('dashboard/contactUs/<str:customerId>',
         views.contactUs, name='contactus')


]
