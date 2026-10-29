from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Booking, Package


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    },
)
class BookingFlowTests(TestCase):
    def test_success_page_redirects_without_a_completed_booking(self):
        response = self.client.get(reverse("bookings:booking_success"))

        self.assertRedirects(response, reverse("bookings:booking"))
        self.assertEqual(Booking.objects.count(), 0)

    def test_success_page_is_available_once_after_valid_booking(self):
        package = Package.objects.create(
            name="Test Package",
            description="Used for booking-flow tests.",
            price="100.00",
            duration_hours=2,
            photo_count=50,
        )
        response = self.client.post(
            reverse("bookings:booking"),
            {
                "name": "Test Customer",
                "phone": "0501234567",
                "email": "",
                "event_type": Booking.EventType.WEDDING,
                "event_date": (timezone.localdate() + timedelta(days=7)).isoformat(),
                "event_location": "Riyadh",
                "package": str(package.pk),
                "notes": "",
            },
        )

        self.assertRedirects(
            response,
            reverse("bookings:booking_success"),
            fetch_redirect_response=False,
        )
        self.assertEqual(Booking.objects.count(), 1)

        success_response = self.client.get(reverse("bookings:booking_success"))
        self.assertEqual(success_response.status_code, 200)
        self.assertContains(success_response, "BOOKING RECEIVED")

        repeat_response = self.client.get(reverse("bookings:booking_success"))
        self.assertRedirects(repeat_response, reverse("bookings:booking"))

    def test_load_demo_packages_is_repeatable_and_does_not_duplicate_records(self):
        call_command("load_demo_packages", verbosity=0)

        self.assertEqual(Package.objects.count(), 3)
        packages = {package.name: package for package in Package.objects.all()}
        self.assertEqual(packages["باقة 100 صورة"].price, 2400)
        self.assertEqual(packages["باقة 100 صورة"].extra_photos, 10)
        self.assertEqual(packages["باقة 70 صورة"].price, 1750)
        self.assertEqual(packages["باقة 50 صورة"].price, 1300)

        call_command("load_demo_packages", verbosity=0)
        self.assertEqual(Package.objects.count(), 3)

    def test_booking_page_shows_empty_state_when_no_packages_exist(self):
        response = self.client.get(reverse("bookings:booking"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "لا توجد باقات متاحة للحجز حاليًا.")
        self.assertContains(response, "disabled")

    def test_invalid_booking_is_not_saved(self):
        package = Package.objects.create(
            name="Validation Package",
            description="Used for form validation tests.",
            price="100.00",
            duration_hours=2,
            photo_count=50,
        )
        response = self.client.post(
            reverse("bookings:booking"),
            {
                "name": "Test Customer",
                "phone": "123",
                "email": "",
                "event_type": Booking.EventType.WEDDING,
                "event_date": (timezone.localdate() + timedelta(days=7)).isoformat(),
                "event_location": "Riyadh",
                "package": str(package.pk),
                "notes": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)
        self.assertContains(response, "رقم الجوال يجب أن يتكون من 10 أرقام.")

    @override_settings(DEBUG=False)
    def test_unknown_url_uses_custom_404_page(self):
        response = self.client.get("/this-url-does-not-exist/")

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "عذرًا، الصفحة غير موجودة", status_code=404)
        self.assertContains(response, "صفحة الحجز", status_code=404)

    def test_theme_selection_sets_a_cookie_and_returns_to_requested_page(self):
        response = self.client.get(
            reverse("bookings:set_theme", args=["dark"]),
            {"next": "/booking/"},
        )

        self.assertRedirects(response, "/booking/")
        self.assertEqual(response.cookies["dst_theme"].value, "dark")
