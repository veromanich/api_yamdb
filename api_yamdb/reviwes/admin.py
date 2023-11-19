from django.contrib import admin

from reviwes.models import User


@admin.register(User)
class PersonAdmin(admin.ModelAdmin):
    pass