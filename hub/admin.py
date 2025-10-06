"""Admin registrations for hub models."""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Community, Person, School


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "availability", "social_links", "created_at")
    list_filter = ("role", "availability")
    search_fields = ("name", "role", "bio", "interests")
    readonly_fields = ("slug", "created_at", "updated_at")
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "role", "bio", "avatar_url")
        }),
        ("Interests & Availability", {
            "fields": ("interests", "availability")
        }),
        ("Social Media", {
            "fields": ("github_url", "twitter_url", "linkedin_url", "website_url"),
            "classes": ("collapse",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        })
    )
    
    def social_links(self, obj):
        """Display social media links as clickable icons."""
        links = obj.get_social_links()
        if not links:
            return "No links"
        
        html_links = []
        for name, url, icon in links:
            html_links.append(
                f'<a href="{url}" target="_blank" rel="noopener noreferrer" '
                f'class="inline-block mr-2 text-blue-500 hover:text-blue-700">{name}</a>'
            )
        return mark_safe("".join(html_links))
    social_links.short_description = "Social Links"
    
    def created_at(self, obj):
        """Show creation date."""
        return obj.pk and obj._state.adding is False
    created_at.boolean = True
    created_at.short_description = "Created"


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "member_count", "founded_year", "contact")
    list_filter = ("location", "founded_year")
    search_fields = ("name", "location", "focus", "description")
    readonly_fields = ("slug", "created_at", "updated_at")
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "location", "contact")
        }),
        ("Description", {
            "fields": ("focus", "description")
        }),
        ("Details", {
            "fields": ("founded_year", "member_count", "logo_url")
        }),
        ("Links", {
            "fields": ("links",),
            "classes": ("collapse",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        })
    )


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "programs_count", "contact")
    list_filter = ("city",)
    search_fields = ("name", "city", "programs")
    readonly_fields = ("slug", "created_at", "updated_at")
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "city", "contact")
        }),
        ("Programs", {
            "fields": ("programs",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        })
    )
    
    def programs_count(self, obj):
        """Show number of programs."""
        return len(obj.programs) if obj.programs else 0
    programs_count.short_description = "Programs"
