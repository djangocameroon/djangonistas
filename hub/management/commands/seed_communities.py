"""Seed Community entries from JSON data."""

from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from hub.models import Community
from hub.utils import load_json_data


class Command(BaseCommand):
    help = "Seed the community directory from data/communities.json."

    def add_arguments(self, parser):
        parser.add_argument(
            "--refresh",
            action="store_true",
            help="Remove existing communities before seeding.",
        )

    def handle(self, *args, **options):
        try:
            payload = load_json_data("communities")
        except FileNotFoundError as exc:
            raise CommandError("Missing data/communities.json. Add the file before seeding.") from exc

        if not isinstance(payload, list):
            raise CommandError("Expected data/communities.json to contain a list of records.")

        if options["refresh"]:
            deleted = Community.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing communities."))

        created_count = 0
        updated_count = 0

        for entry in payload:
            name = entry.get("name")
            if not name:
                self.stdout.write(self.style.WARNING("Skipped entry without a name."))
                continue

            defaults = {
                "focus": entry.get("focus", ""),
                "location": entry.get("location", ""),
                "contact": entry.get("contact", ""),
                "links": entry.get("links", {}),
                "logo_url": entry.get("logo_url", ""),
                "description": entry.get("description", ""),
                "founded_year": entry.get("founded_year"),
                "member_count": entry.get("member_count"),
            }
            _, created = Community.objects.update_or_create(name=name, defaults=defaults)
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete. Created {created_count} and updated {updated_count} community entries."
            )
        )
