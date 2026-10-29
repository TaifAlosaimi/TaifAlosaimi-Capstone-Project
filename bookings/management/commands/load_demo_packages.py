from django.core.management.base import BaseCommand

from bookings.models import Package


DEMO_PACKAGES = (
    {
        "name": "باقة 100 صورة",
        "description": "100 صورة مطبوعة + 10 مجانًا، شامل حامل الصور (Card) بثيم المناسبة.",
        "price": "2400.00",
        "duration_hours": 4,
        "photo_count": 100,
        "extra_photos": 10,
    },
    {
        "name": "باقة 70 صورة",
        "description": "70 صورة مطبوعة، شامل حامل الصور (Card) بثيم المناسبة.",
        "price": "1750.00",
        "duration_hours": 3,
        "photo_count": 70,
        "extra_photos": 0,
    },
    {
        "name": "باقة 50 صورة",
        "description": "50 صورة مطبوعة، شامل حامل الصور (Card) بثيم المناسبة.",
        "price": "1300.00",
        "duration_hours": 2,
        "photo_count": 50,
        "extra_photos": 0,
    },
)


class Command(BaseCommand):
    help = "Create any missing approved DST demo packages without overwriting existing packages."

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for package_data in DEMO_PACKAGES:
            name = package_data["name"]
            if Package.objects.filter(name=name).exists():
                skipped_count += 1
                self.stdout.write(f"Skipped existing package: {name}")
                continue

            Package.objects.create(**package_data)
            created_count += 1
            self.stdout.write(f"Created package: {name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo package setup complete. Created: {created_count}; skipped existing: {skipped_count}."
            )
        )
