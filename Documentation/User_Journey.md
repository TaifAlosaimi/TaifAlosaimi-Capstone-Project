# User Journey — DST Photobooth

## Customer journey

1. **Discover DST** — The visitor opens the home page and sees the brand introduction and links to learn more or start a booking.
2. **Learn about the service** — The visitor opens the About page to read about the photobooth experience and service area.
3. **Open the booking form** — The visitor opens `/booking/`. The page renders package records from the `Package` queryset available to `BookingForm`.
4. **Choose a package** — The visitor selects one existing package. The package choice is submitted as part of the form; it is not a separate payment or checkout flow.
5. **Enter event details** — The visitor chooses an event type, selects a future event date, enters the event location, name and Saudi-format mobile number, and may add an email address and notes.
6. **Submit the request** — The browser sends a POST request with a CSRF token. `BookingForm` validates the submitted values on the server.
7. **Handle validation** — If validation fails, Django renders the booking page again with the bound form and its field errors. The visitor can correct the fields and resubmit.
8. **Save the booking** — If validation succeeds, `form.save()` creates a `Booking`. The model's default status is `Pending` and `created_at` is populated automatically.
9. **Show the confirmation page** — The view sets `request.session["booking_success"] = True` and redirects to `/booking/success/`. The success view consumes that flag and renders the success template.
10. **Manage requests (staff)** — An authorized administrator can use Django Admin at `/admin/` to review booking records, update their status, and manage package records.

## Theme preference journey

1. The visitor selects the light or dark theme control.
2. The browser requests the theme route with the chosen theme and the current path as `next`.
3. The view accepts only `light` or `dark`, validates that `next` is a safe same-host destination, sets the `dst_theme` cookie for 30 days, and redirects back to the requested page (or home if the destination is not allowed).
4. The shared base template reads the cookie to set the page's `data-theme` attribute.

## Scope notes

- The website records a **booking request**; the success message says DST will contact the customer to confirm details. A successful form submission does not mean the booking status is already `Confirmed`.
- The current implementation does not show a payment step, customer account registration, automated availability calendar, or double-booking prevention. These should not be described as current features.
