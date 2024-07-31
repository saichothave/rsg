from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RSGUser, ShopOwner, BillingDesk, Scanner
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

# Register your models here.
# admin.site.register(RSGUser)


class ShopOwnerAdmin(ModelAdmin):
    model = ShopOwner
    search_fields = ['user', 'shop_name', 'city']
    ordering =  ['user']

class BillingDeskAdmin(ModelAdmin):
    model = BillingDesk
    search_fields = ['user']
    ordering =  ['user']

class ScannerAdmin(ModelAdmin):
    model = Scanner
    search_fields = ['user']
    ordering =  ['user']

class CustomUserAdmin(UserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )

admin.site.register(RSGUser, CustomUserAdmin)
admin.site.register(ShopOwner, ShopOwnerAdmin)
admin.site.register(BillingDesk, BillingDeskAdmin)
admin.site.register(Scanner, ScannerAdmin)