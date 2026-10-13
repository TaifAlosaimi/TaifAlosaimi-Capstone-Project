from django.urls import path

from . import views


app_name = "bookings"


urlpatterns = [
    path("theme/<str:theme>/", views.set_theme, name="set_theme"),
    path("booking/", views.booking_create, name="booking"),
    path(
        "booking/success/",
        views.booking_success,
        name="booking_success",
    ),
]

