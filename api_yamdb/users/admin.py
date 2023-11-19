from django.contrib import admin

from users.models import User


@admin.register(User)
class PersonAdmin(admin.ModelAdmin):
    pass
