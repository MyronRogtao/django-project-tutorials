from django.contrib import admin
from .models import Realtor


class RealtorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_mvp', 'hire_date')
    list_display_links = ('name',)
    list_filter = ('name', 'email', 'phone', 'is_mvp', 'hire_date')
    list_editable = ('is_mvp',)
    search_fields = ('name', 'email', 'phone')
    list_per_page = 25


# Register your models here.
admin.site.register(Realtor, RealtorAdmin)
