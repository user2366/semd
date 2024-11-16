from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Semd


class MyDashboard(admin.ModelAdmin):
    model = Semd
    list_display = ['lid', 'status']
    search_fields = ['lid', 'status']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Semd, MyDashboard)