from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Booking, Package


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

        self.assertRedirects(response, reverse("bookings:booking_success"))
        self.assertEqual(Booking.objects.count(), 1)

        success_response = self.client.get(reverse("bookings:booking_success"))
        self.assertEqual(success_response.status_code, 200)
        self.assertContains(success_response, "BOOKING RECEIVED")

        repeat_response = self.client.get(reverse("bookings:booking_success"))
        self.assertRedirects(repeat_response, reverse("bookings:booking"))

    def test_theme_selection_sets_a_cookie_and_returns_to_requested_page(self):
        response = self.client.get(
            reverse("bookings:set_theme", args=["dark"]),
            {"next": "/booking/"},
        )

        self.assertRedirects(response, "/booking/")
        self.assertEqual(response.cookies["dst_theme"].value, "dark")
