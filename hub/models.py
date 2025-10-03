"""Data models backing the community directory."""

from __future__ import annotations

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class SluggedModel(models.Model):
    """Abstract base model adding a unique slug derived from the name."""

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True, editable=False, blank=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.name:
            raise ValueError("Name is required to generate a slug.")

        base_slug = slugify(self.name)
        if not base_slug:
            raise ValueError("Unable to derive slug from name.")

        slug = base_slug
        counter = 1
        ModelClass = type(self)

        while ModelClass.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            counter += 1
            slug = f"{base_slug}-{counter}"

        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover - human-friendly repr
        return self.name


class Person(SluggedModel):
    role = models.CharField(max_length=120)
    interests = models.JSONField(default=list, blank=True)
    availability = models.CharField(max_length=200, blank=True)
    avatar_url = models.URLField(blank=True, help_text="Link to profile photo/avatar")
    bio = models.TextField(blank=True, help_text="Short bio or description")
    
    # Social media links
    github_url = models.URLField(blank=True, help_text="GitHub profile URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter/X profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    website_url = models.URLField(blank=True, help_text="Personal website URL")

    def get_absolute_url(self) -> str:
        return reverse("hub:person-detail", kwargs={"slug": self.slug})


class Community(SluggedModel):
    focus = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    contact = models.CharField(max_length=150, blank=True)
    links = models.JSONField(default=dict, blank=True)
    logo_url = models.URLField(blank=True, help_text="Link to community logo/image")
    description = models.TextField(blank=True, help_text="Detailed community description")
    founded_year = models.IntegerField(blank=True, null=True, help_text="Year the community was founded")
    member_count = models.IntegerField(blank=True, null=True, help_text="Approximate number of members")

    def get_absolute_url(self) -> str:
        return reverse("hub:community-detail", kwargs={"slug": self.slug})


class School(SluggedModel):
    city = models.CharField(max_length=120, blank=True)
    programs = models.JSONField(default=list, blank=True)
    contact = models.CharField(max_length=150, blank=True)

    def get_absolute_url(self) -> str:
        return reverse("hub:school-detail", kwargs={"slug": self.slug})
