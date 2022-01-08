from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', "first_name","email")  # 'username',
    list_display_links = ("username", "email")
    list_filter = ('is_active', )
    search_fields = ('username', 'email', 'status')
    exclude = ('is_active', )

admin.site.register((Jwt, UserProfile))
