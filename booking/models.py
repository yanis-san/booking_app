from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime


class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AppointmentDatetime(models.Model):
    thedatetime = models.DateTimeField()
    is_bookable = models.BooleanField(default=True)

    @staticmethod
    def get_dates_times():
        available_date = AppointmentDatetime.objects.filter(
            is_bookable=True
        ).values_list("thedatetime", flat=True)

        dates = [date.date().strftime("%Y-%m-%d") for date in available_date]
        time_slots = [time.time().strftime("%H:%M") for time in available_date]

        return dates, time_slots

    def __str__(self):
        return self.thedatetime.strftime("%Y-%m-%d %H:%M")


class Appointment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)
    is_passed = models.BooleanField(default=False)
    appointment_datetime = models.ForeignKey(
        to=AppointmentDatetime, on_delete=models.CASCADE
    )

    @staticmethod
    def make_datetime(date, time):
        datetime_str = f"{date} {time}"

        appointment_datetime = datetime.strptime(
            datetime_str, "%Y-%m-%d %H:%M"
        )
        return appointment_datetime

    @staticmethod
    def user_service_exist(user, service):
        if Appointment.objects.filter(user=user, service=service).exists():
            return True
        else:
            return False

    def __str__(self):
        return f"{self.user.username} {self.appointment_datetime}"
