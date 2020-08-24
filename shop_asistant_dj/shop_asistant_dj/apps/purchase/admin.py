from django.contrib import admin
from .models import Purchase, PurchasesList

admin.site.register(PurchasesList)
admin.site.register(Purchase)
