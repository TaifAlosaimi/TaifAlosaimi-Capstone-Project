# Business Rules — DST Photobooth

This document describes rules supported by the current Django implementation. Rules enforced only by the form are identified as form-level rules; they are not claimed to be database constraints.

## 1. Packages

- A package stores its name, description, price, duration in hours, number of photos, and optional extra-photo count.
- `price` must be zero or greater. This is enforced by a database `CheckConstraint` named `package_price_nonnegative`.
- `duration_hours` must be greater than zero. The model uses `PositiveIntegerField` and also defines the database check `package_duration_positive`.
- `photo_count` must be greater than zero. The model uses `PositiveIntegerField` and also defines the database check `package_photo_count_positive`.
- `extra_photos` defaults to `0` and uses `PositiveIntegerField`.
- The current model does not enforce unique package names or a fixed list of package prices/counts.

## 2. Booking details and form validation

- A booking must include a name (up to 100 characters), a phone number, an event type, an event date, an event location (up to 200 characters), and a selected package.
- The booking form requires the phone number to be exactly 10 digits and match `^05[0-9]{8}$` (Saudi mobile format beginning with `05`). This rule is enforced by `BookingForm`, not by a model/database constraint; the model field itself allows up to 20 characters.
- Email is optional. If supplied, it must be a valid email address according to Django's `EmailField` validation.
- Notes are optional.
- Event type must be one of the model choices: Wedding, Graduation, Corporate Event, Brand Event, or Other.
- The booking form allows only event dates after the current date in `Asia/Riyadh`. The HTML date input also receives a minimum date of tomorrow, and `clean_event_date()` validates the rule server-side.
- The selected package must be an existing `Package` record accepted by the ModelForm choice field.

## 3. Booking status and persistence

- A newly created booking defaults to `Pending`.
- The model defines the status choices `Pending`, `Confirmed`, and `Cancelled`.
- A valid POST request is saved as a `Booking` and then redirected to the named booking-success route.
- The success view uses the session flag `booking_success` to show the success page after a successful form submission. If the flag is absent, the visitor is redirected to the booking page; the flag is removed when read, so the success page is intended to be shown once.
- The booking records the creation timestamp automatically in `created_at`.

## 4. Package–Booking relationship

- Each `Booking` must reference exactly one `Package` through the required `package` ForeignKey (`null=False` by default).
- A `Package` may have zero, one, or many related bookings.
- `on_delete=models.PROTECT` prevents deletion of a package while booking records reference it.
- There is no explicit database rule preventing overlapping bookings for the same event date, limiting bookings per day, or automatically confirming a booking. Do not assume those behaviours exist.

## 5. Theme preference

- Visitors may choose `light` or `dark` through the theme route.
- The selected theme is stored in the `dst_theme` cookie for 30 days.
- The view validates the theme value and checks the `next` URL against the current host before redirecting, falling back to the home route if the destination is not allowed.

## Enforcement summary

| Rule | Enforcement in current code |
|---|---|
| Package price is non-negative | Database check constraint |
| Package duration and photo count are positive | PositiveIntegerField and database check constraints |
| Phone uses Saudi `05xxxxxxxx` format | BookingForm validator |
| Event date is after today in Riyadh | BookingForm server-side validation and date-input minimum |
| Email may be blank but must be valid if supplied | BookingForm / EmailField validation |
| Event type and status use defined choices | Django model/form choices; not a database enum constraint |
| Booking requires one existing package | Required ForeignKey and ModelForm validation |
| Referenced package cannot be deleted | `on_delete=PROTECT` |
| New booking starts as Pending | Model default |
