from django.contrib import admin
from .models import userdata, Listing, Review

# Register your models here.
admin.site.register(userdata)
admin.site.register(Listing)
admin.site.register(Review)
