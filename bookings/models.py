from django.db import models


class Package(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_hours = models.PositiveIntegerField()
    photo_count = models.PositiveIntegerField()
    extra_photos = models.PositiveIntegerField(default=0)


    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="package_price_nonnegative",
            ),
            models.CheckConstraint(
                condition=models.Q(duration_hours__gt=0),
                name="package_duration_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(photo_count__gt=0),
                name="package_photo_count_positive",
            ),
        ]


    def __str__(self):
        return self.name


class Booking(models.Model):

    class EventType(models.TextChoices):
        WEDDING = "Wedding", "زواج"
        GRADUATION = "Graduation", "تخرج"
        CORPORATE = "Corporate Event", "فعالية شركات"
        BRAND = "Brand Event", "فعالية علامة تجارية"
        OTHER = "Other", "أخرى"

    class Status(models.TextChoices):
        PENDING = "Pending", "قيد المراجعة"
        CONFIRMED = "Confirmed", "مؤكد"
        CANCELLED = "Cancelled", "ملغي"

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    event_type = models.CharField(
        max_length=30,
        choices=EventType.choices
    )
    event_date = models.DateField()
    event_location = models.CharField(max_length=200)
    package = models.ForeignKey(
        Package,
        on_delete=models.PROTECT,
        related_name="bookings"
    )
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.package.name}"