from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RSGUser, ShopOwner, BillingDesk, Scanner

# Register your models here.
# admin.site.register(RSGUser)


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )

admin.site.register(RSGUser, CustomUserAdmin)
admin.site.register(ShopOwner)
admin.site.register(BillingDesk)
admin.site.register(Scanner)