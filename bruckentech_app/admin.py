from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("tx_ref", "email", "amount", "status", "created_at")
    search_fields = ("tx_ref", "email")
    list_filter = ("status",)
