from django.contrib import admin

# Register your models here.
from .models import OutfitPlan, LookItem

admin.site.register(OutfitPlan)
admin.site.register(LookItem)
