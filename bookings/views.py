
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import BookingForm


def home(request):
    return render(request, "bookings/home.html")

def about(request):
    return render(request, "bookings/about.html")

def booking_create(request):
    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            form.save()
            request.session["booking_success"] = True
            return redirect("bookings:booking_success")
    else:
        form = BookingForm()

    return render(request, "bookings/booking.html", {"form": form})

def booking_success(request):
    # Show this page only once, immediately after a successful booking.
    if not request.session.pop("booking_success", False):
        return redirect("bookings:booking")

    return render(request, "bookings/booking_success.html")

def set_theme(request, theme):
    """Save the visitor's selected color theme in a cookie."""
    if theme not in {"light", "dark"}:
        return redirect("home")

    next_url = request.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = reverse("home")

    response = redirect(next_url)
    response.set_cookie(
        "dst_theme",
        theme,
        max_age=60 * 60 * 24 * 30,
        httponly=True,
        samesite="Lax",
        secure=not settings.DEBUG,
    )
    return response
