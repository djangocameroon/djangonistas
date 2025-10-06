"""Data models backing the community directory."""

from __future__ import annotations

from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import format_html


class SluggedModel(models.Model):
    """Abstract base model adding a unique slug derived from the name."""

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True, editable=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    role = models.CharField(max_length=120, help_text="Professional role or title")
    interests = models.JSONField(default=list, blank=True, help_text="List of interests and skills")
    availability = models.CharField(max_length=200, blank=True, help_text="What they're available for")
    avatar_url = models.URLField(blank=True, help_text="Link to profile photo/avatar")
    bio = models.TextField(blank=True, help_text="Short bio or description")
    
    # Social media links
    github_url = models.URLField(blank=True, help_text="GitHub profile URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter/X profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    website_url = models.URLField(blank=True, help_text="Personal website URL")

    class Meta:
        ordering = ["name"]
        verbose_name = "Person"
        verbose_name_plural = "People"

    def clean(self):
        """Validate the model instance."""
        super().clean()
        
        # Validate URLs if provided
        url_validator = URLValidator()
        for field_name in ['avatar_url', 'github_url', 'twitter_url', 'linkedin_url', 'website_url']:
            url = getattr(self, field_name)
            if url:
                try:
                    url_validator(url)
                except ValidationError:
                    raise ValidationError({field_name: f"Enter a valid URL for {field_name}."})
        
        # Validate interests is a list
        if not isinstance(self.interests, list):
            raise ValidationError({'interests': 'Interests must be a list of strings.'})

    def get_social_links(self):
        """Return a list of non-empty social media links."""
        links = []
        if self.github_url:
            links.append(('GitHub', self.github_url, 'github'))
        if self.twitter_url:
            links.append(('Twitter', self.twitter_url, 'twitter'))
        if self.linkedin_url:
            links.append(('LinkedIn', self.linkedin_url, 'linkedin'))
        if self.website_url:
            links.append(('Website', self.website_url, 'website'))
        return links

    def get_avatar_display(self):
        """Return HTML for avatar display."""
        if self.avatar_url:
            return format_html(
                '<img src="{}" alt="{}" class="h-16 w-16 rounded-full object-cover">',
                self.avatar_url, self.name
            )
        else:
            return format_html(
                '<div class="flex h-16 w-16 items-center justify-center rounded-full bg-sky-500/20 text-lg font-bold text-sky-200">{}</div>',
                self.name[0].upper()
            )

    def get_absolute_url(self) -> str:
        return reverse("hub:person-detail", kwargs={"slug": self.slug})


class Community(SluggedModel):
    focus = models.TextField(blank=True, help_text="Main focus or mission of the community")
    location = models.CharField(max_length=120, blank=True, help_text="Physical location or region")
    contact = models.CharField(max_length=150, blank=True, help_text="Contact email or information")
    links = models.JSONField(default=dict, blank=True, help_text="Social media and website links")
    logo_url = models.URLField(blank=True, help_text="Link to community logo/image")
    description = models.TextField(blank=True, help_text="Detailed community description")
    founded_year = models.IntegerField(
        blank=True, 
        null=True, 
        help_text="Year the community was founded",
        validators=[MinValueValidator(1900), MaxValueValidator(2030)]
    )
    member_count = models.IntegerField(
        blank=True, 
        null=True, 
        help_text="Approximate number of members",
        validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Community"
        verbose_name_plural = "Communities"

    def clean(self):
        """Validate the model instance."""
        super().clean()
        
        # Validate URLs if provided
        url_validator = URLValidator()
        for field_name in ['logo_url']:
            url = getattr(self, field_name)
            if url:
                try:
                    url_validator(url)
                except ValidationError:
                    raise ValidationError({field_name: f"Enter a valid URL for {field_name}."})
        
        # Validate links is a dict
        if not isinstance(self.links, dict):
            raise ValidationError({'links': 'Links must be a dictionary.'})

    def get_links_display(self):
        """Return a list of non-empty links."""
        links = []
        if self.links.get('website'):
            links.append(('Website', self.links['website'], 'website'))
        if self.links.get('twitter'):
            links.append(('Twitter', self.links['twitter'], 'twitter'))
        if self.links.get('linkedin'):
            links.append(('LinkedIn', self.links['linkedin'], 'linkedin'))
        return links

    def get_logo_display(self):
        """Return HTML for logo display."""
        if self.logo_url:
            return format_html(
                '<img src="{}" alt="{}" class="h-16 w-16 rounded-lg object-cover">',
                self.logo_url, self.name
            )
        else:
            return format_html(
                '<div class="flex h-16 w-16 items-center justify-center rounded-lg bg-purple-500/20 text-lg font-bold text-purple-200">{}</div>',
                self.name[0].upper()
            )

    def get_absolute_url(self) -> str:
        return reverse("hub:community-detail", kwargs={"slug": self.slug})


class School(SluggedModel):
    city = models.CharField(max_length=120, blank=True, help_text="City where the school is located")
    programs = models.JSONField(default=list, blank=True, help_text="List of programs offered")
    contact = models.CharField(max_length=150, blank=True, help_text="Contact information")

    class Meta:
        ordering = ["name"]
        verbose_name = "School"
        verbose_name_plural = "Schools"

    def clean(self):
        """Validate the model instance."""
        super().clean()
        
        # Validate programs is a list
        if not isinstance(self.programs, list):
            raise ValidationError({'programs': 'Programs must be a list of strings.'})

    def get_programs_display(self):
        """Return a formatted string of programs."""
        if not self.programs:
            return "No programs listed"
        return ", ".join(self.programs)

    def get_absolute_url(self) -> str:
        return reverse("hub:school-detail", kwargs={"slug": self.slug})
