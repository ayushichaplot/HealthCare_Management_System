from django.contrib import admin

# Register your models here.
from . models import Patient , Visit
admin.site.register(Patient)
admin.site.register(Visit)