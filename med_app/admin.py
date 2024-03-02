from django.contrib import admin
from .models import *


class DateInline(admin.TabularInline):
    model = Date
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["user_id", "username", "is_doctor"]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ["user", "full_name"]
    list_display_links = ["user", "full_name"]
    readonly_fields = ['activate_url']

    inlines = [DateInline]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["user", "full_name", "confirance_status"]


@admin.register(PatientResult)
class PatientResultAdmin(admin.ModelAdmin):
    list_display = ["patient", "doctor"]


@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    list_display = ["patient", "doctor"]


@admin.register(BotAdmin)
class BotAdminAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at"]


@admin.register(DoctorRating)
class DoctorRatingAdmin(admin.ModelAdmin):
    list_display = ["doctor", "rating"]


@admin.register(ChatStorage)
class ChatStorageAdmin(admin.ModelAdmin):
    list_display = ["doctor", "patient", "created_at"]


@admin.register(PatientPayment)
class PatientPaymentAdmin(admin.ModelAdmin):
    list_display = ["doctor", "patient", "paid"]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "created_at"]


@admin.register(CallNotification)
class CallNotificationAdmin(admin.ModelAdmin):
    list_display = ["patient", "message_id"]


