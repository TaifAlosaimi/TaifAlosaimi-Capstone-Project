from django.contrib import admin
from django.db.models import Count, Sum

from .models import Booking, Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "duration_hours",
        "photo_count",
        "booking_count",
    )
    search_fields = ("name", "description")
    list_filter = ("duration_hours",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            booking_count=Count("bookings")
        )

    @admin.display(description="عدد الحجوزات")
    def booking_count(self, obj):
        return obj.booking_count


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "event_type",
        "event_date",
        "package",
        "status",
        "created_at",
    )
    search_fields = ("name", "phone", "email", "event_location")
    list_filter = ("status", "event_type", "event_date", "package")
    ordering = ("-created_at",)
    date_hierarchy = "event_date"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        confirmed_bookings = self.get_queryset(request).filter(
            status=Booking.Status.CONFIRMED
        )

        extra_context["confirmed_booking_count"] = (
            confirmed_bookings.count()
        )
        extra_context["confirmed_booking_value"] = (
            confirmed_bookings.aggregate(
                total=Sum("package__price")
            )["total"] or 0
        )

        return super().changelist_view(
            request,
            extra_context=extra_context,
        )
