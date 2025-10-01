"""Admin registrations for hub models."""

from django.contrib import admin

from .models import Community, Person, School


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "availability")
    search_fields = ("name", "role", "availability")
    readonly_fields = ("slug",)


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "contact")
    search_fields = ("name", "location", "contact")
    readonly_fields = ("slug",)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "contact")
    search_fields = ("name", "city", "contact")
    readonly_fields = ("slug",)
