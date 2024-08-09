from django import forms
from booking.models import Appointment, AppointmentDatetime
from datetime import time, date, timedelta


        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service','appointment_datetime']
        widgets = {
            'appointment_datetime': forms.TextInput(attrs={
                'id': 'datetime',
                'placeholder': 'Selectionnez une date',
                'class': 'block w-full px-2 border-gray-300 focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 rounded-l-md shadow-sm',
                'required': True
            })
               }




