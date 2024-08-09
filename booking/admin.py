from django.contrib import admin
from booking.models import Appointment, AppointmentDatetime,Service

# @admin.register(Appointment)
# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = ('date', 'is_available', 'email')
#     list_filter = ('is_available',)
#     search_fields = ('date',)


admin.site.register(Appointment)
admin.site.register(AppointmentDatetime)
admin.site.register(Service)