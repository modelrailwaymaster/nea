from django.contrib import admin
from .models import listing, user_saved

# Register your models here.

admin.site.register(listing)
admin.site.register(user_saved)
