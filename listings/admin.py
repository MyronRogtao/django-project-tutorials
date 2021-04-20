from django.contrib import admin
from .models import Listing, ListingImage, Enquiry


# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'description', 'list_date', 'address', 'realtor', 'bedrooms', 'bathrooms')
    list_display_links = ('title',)
    list_filter = ('title', 'is_published', 'description', 'list_date', 'realtor', 'bedrooms', 'bathrooms')
    list_editable = ('is_published',)
    search_fields = ('title', 'description', 'realtor__name', 'address', 'city', 'price')
    list_per_page = 25

admin.site.register(Listing, ListingAdmin)
admin.site.register(ListingImage)
admin.site.register(Enquiry)
