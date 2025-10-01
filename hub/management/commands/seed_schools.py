"""Seed School entries from JSON data."""

from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from hub.models import School
from hub.utils import load_json_data


class Command(BaseCommand):
    help = "Seed the school directory from data/schools.json."

    def add_arguments(self, parser):
        parser.add_argument(
            "--refresh",
            action="store_true",
            help="Remove existing schools before seeding.",
        )

    def handle(self, *args, **options):
        try:
            payload = load_json_data("schools")
        except FileNotFoundError as exc:
            raise CommandError("Missing data/schools.json. Add the file before seeding.") from exc

        if not isinstance(payload, list):
            raise CommandError("Expected data/schools.json to contain a list of records.")

        if options["refresh"]:
            deleted = School.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing schools."))

        created_count = 0
        updated_count = 0

        for entry in payload:
            name = entry.get("name")
            if not name:
                self.stdout.write(self.style.WARNING("Skipped entry without a name."))
                continue

            defaults = {
                "city": entry.get("city", ""),
                "programs": entry.get("programs", []),
                "contact": entry.get("contact", ""),
            }
            _, created = School.objects.update_or_create(name=name, defaults=defaults)
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete. Created {created_count} and updated {updated_count} school entries."
            )
        )
