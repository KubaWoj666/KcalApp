from django.contrib import admin

from .models import UserAccount, WeightEntry

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "role", "is_active", "is_staff","is_pro", "height", "weight"]
    

class WeightEntryAdmin(admin.ModelAdmin):
    list_display = ["user", "date", "weight"]

admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(WeightEntry, WeightEntryAdmin)