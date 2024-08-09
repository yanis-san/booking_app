from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, Service, AppointmentDatetime
from .forms import AppointmentForm
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse, HttpResponse

@login_required
def booking(request):
    dates, time_slot = AppointmentDatetime.get_dates_times()

    if request.method == "POST":
        thedatetime = Appointment.make_datetime(
            request.POST.get("appointment_datetime"),
            request.POST.get("time_slot"),
        )

        try:
            appointment_datetime_instance = AppointmentDatetime.objects.get(
                thedatetime=thedatetime
            )
        except AppointmentDatetime.DoesNotExist:
            return render(request, 'booking/booking_confirm.html', {
                "message": "La date et l'heure fournies ne correspondent à aucune instance disponible."
            })

        new_post_data = request.POST.copy()
        new_post_data["appointment_datetime"] = appointment_datetime_instance.id
        new_post_data.pop("time_slot", None)
        form = AppointmentForm(new_post_data)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            if Appointment.user_service_exist(request.user, new_post_data["service"]):
                return render(request, 'booking/booking_confirm.html', {
                    "success": False
                })
            else:
                appointment.save()
                appointment_datetime_instance.is_bookable = False
                appointment_datetime_instance.save()
                return render(request, 'booking/booking_confirm.html', {
                    "success":True
                })

    return render(
        request,
        "booking/booking.html",
        {"form": AppointmentForm(), "dates": dates, "time_slot": time_slot},
    )

def get_times(request):
    date = request.GET.get("date")
    if date:
        available_times = AppointmentDatetime.objects.filter(
            thedatetime__date=date, is_bookable=True
        ).values_list("thedatetime", flat=True)

        time_slots = [
            time.time().strftime("%H:%M") for time in available_times
        ]
    else:
        time_slots = []

    return render(
        request, "booking/time_slots.html", {"time_slots": time_slots}
    )