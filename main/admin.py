from django.contrib import admin

from .models import Employee, Sector, Department, Card

admin.site.register([Employee,Sector,Department, Card])