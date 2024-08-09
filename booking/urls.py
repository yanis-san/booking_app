from django.urls import path 
from booking.views import booking, get_times

app_name="booking"

urlpatterns = [


    path('', booking, name='booking'),
    path('get-times/', get_times, name='get_times'),
    

    

]