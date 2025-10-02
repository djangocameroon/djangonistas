"""Seed Person entries from JSON data."""

from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from hub.models import Person
from hub.utils import load_json_data


class Command(BaseCommand):
    help = "Seed the people directory from data/people.json."

    def add_arguments(self, parser):
        parser.add_argument(
            "--refresh",
            action="store_true",
            help="Remove existing people before seeding.",
        )

    def handle(self, *args, **options):
        try:
            payload = load_json_data("people")
        except FileNotFoundError as exc:
            raise CommandError("Missing data/people.json. Add the file before seeding.") from exc

        if not isinstance(payload, list):
            raise CommandError("Expected data/people.json to contain a list of records.")

        if options["refresh"]:
            deleted = Person.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing people."))

        created_count = 0
        updated_count = 0

        for entry in payload:
            name = entry.get("name")
            if not name:
                self.stdout.write(self.style.WARNING("Skipped entry without a name."))
                continue

            defaults = {
                "role": entry.get("role", ""),
                "interests": entry.get("interests", []),
                "availability": entry.get("availability", ""),
                "avatar_url": entry.get("avatar_url", ""),
                "bio": entry.get("bio", ""),
                "github_url": entry.get("github_url", ""),
                "twitter_url": entry.get("twitter_url", ""),
                "linkedin_url": entry.get("linkedin_url", ""),
                "website_url": entry.get("website_url", ""),
            }
            _, created = Person.objects.update_or_create(name=name, defaults=defaults)
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete. Created {created_count} and updated {updated_count} people entries."
            )
        )
