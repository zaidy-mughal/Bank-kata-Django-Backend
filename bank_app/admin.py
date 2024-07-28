from django.contrib import admin
from .models import Account, Movement

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["id","name","balance","is_IBAN","IBAN"]

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ["account","movement_type","date","amount","balance"]

