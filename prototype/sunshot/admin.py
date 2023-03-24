from django.contrib import admin
from sunshot.models import Account

# Register your models here.


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "level",
        "xp",
        "verified",
    )
