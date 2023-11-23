from django.contrib import admin

from users.models import User


@admin.register(User)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role',)
    list_display_links = None
    list_editable = ('role',)
