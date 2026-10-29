# DST Photobooth

An Arabic-first Django website for DST Photobooth. Visitors can learn about the service, review photobooth packages, and submit an event booking request. Staff manage packages and booking records through Django Admin.

**Source repository:** [TaifAlosaimi/TaifAlosaimi-Capstone-Project](https://github.com/TaifAlosaimi/TaifAlosaimi-Capstone-Project) — includes the project's Git commit history.

## Project overview

The site uses a premium editorial visual style and a responsive layout. Its main workflow is a booking request: the visitor chooses an existing package, submits event and contact details, Django validates the form, and a valid request is saved with the initial status `Pending`. The success page explains that DST will contact the customer to confirm the details; submission is not the same as final booking confirmation.

## Current functionality

- Home and About pages.
- Booking form populated from database-backed `Package` records.
- Server-side Django form validation and CSRF protection.
- Booking success flow guarded by a session flag so direct/repeated visits do not display the success page as if a booking had just been submitted.
- Django Admin management for packages and bookings, including filters/search and booking summary values.
- Light/dark theme preference stored in the `dst_theme` cookie for 30 days.
- Custom 404 template and handler are present in the code. With Django `DEBUG=True`, the development server displays Django's technical 404 page instead of the custom page; test the custom 404 with `DEBUG=False` and a valid local secret/host configuration.

## Technology stack

- Python 3.14.6 (the version used in the supplied project virtual environment)
- Django 6.1.1 (pinned in `requirements.txt`)
- Django ORM
- SQLite by default for local development; `DATABASE_URL` can configure a different database
- HTML and CSS
- WhiteNoise for static files in deployment
- `dj-database-url` for database URL configuration

## Data model and relationship

The database has two application models:

- **Package**: `name`, `description`, `price`, `duration_hours`, `photo_count`, `extra_photos`.
- **Booking**: contact details, event type/date/location, optional notes, status, creation timestamp, and a foreign key to `Package`.

Relationship: **Package 1 → 0..* Booking**. Every booking must reference exactly one package; a package can have no bookings or many bookings. `Booking.package` uses `on_delete=PROTECT`, so a package referenced by a booking cannot be deleted.

See [`Documentation/ERD.png`](Documentation/ERD.png), [`Documentation/Business_Rules.md`](Documentation/Business_Rules.md), and [`Documentation/User_Journey.md`](Documentation/User_Journey.md) for the model diagram, verified business rules, and user journey.

## Booking rules (summary)

- A booking requires name, phone, event type, event date, event location, and package.
- The form validates the mobile number as 10 digits beginning with `05`.
- Email and notes are optional; a provided email must be valid.
- Event date must be after today's date in the `Asia/Riyadh` timezone.
- New bookings default to `Pending`; staff can manage status in Django Admin.
- Package price must be non-negative, and duration/photo count must be positive; these are backed by database constraints.

For the full enforcement details, including which rules are form-level versus database-level, read `Documentation/Business_Rules.md`. For a repeatable set of fictional demo records, see `Documentation/Sample_Data.md`.

## Project structure

```text
DST/
├── bookings/
│   ├── migrations/
│   ├── management/commands/load_demo_packages.py
│   ├── static/bookings/
│   ├── templates/bookings/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── dst_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── Documentation/
│   ├── ERD.png
│   ├── Business_Rules.md
│   ├── Sample_Data.md
│   ├── User_Journey.md
│   └── Verification_Record.md
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup and run locally

Commands below are for Windows PowerShell, from the directory containing `manage.py`.

1. **Create and activate a virtual environment**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. **Configure the Django secret key**

   Generate a key:

   ```powershell
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Create `secret_key.txt` in the project root and paste the generated key into it. The settings file reads this local file when the `SECRET_KEY` environment variable is not set. Never commit the secret key or share it publicly.

4. **Apply database migrations**

   ```powershell
   python manage.py migrate
   ```

5. **Collect static files**

   This project uses WhiteNoise with a compressed manifest storage backend. Run this after migrations and whenever static assets change, especially before testing with `DEBUG=False` or preparing a deployment.

   ```powershell
   python manage.py collectstatic --noinput
   ```

6. **Load the approved demo packages**

   A fresh database has no package records after migrations alone. Create the three approved DST packages with:

   ```powershell
   python manage.py load_demo_packages
   ```

   The command adds only packages that are missing by name. It does not overwrite existing package records, and it is safe to run again. Review `Documentation/Sample_Data.md` for the package values and optional fictional booking data used for the demo.

7. **Create an administrator account (optional, for Django Admin)**

   ```powershell
   python manage.py createsuperuser
   ```

8. **Run the development server**

   ```powershell
   python manage.py runserver
   ```

   Open `http://127.0.0.1:8000/`. The booking page should now show the demo packages.

### Verify the branded 404 page locally

Django intentionally displays its technical 404 page while `DEBUG=True`. To verify the branded page, first collect static files, then run the server with debug disabled. Run these commands in the same PowerShell terminal from the project root:

```powershell
python manage.py collectstatic --noinput
$env:DEBUG = "False"
python manage.py runserver
```

Open `http://127.0.0.1:8000/this-url-does-not-exist/`. The expected result is the Arabic DST 404 page and an HTTP `404` response. When finished, stop the server and restore the development setting in that terminal with `$env:DEBUG = "True"` before running the server again. Do not use `DEBUG=False` without a valid `SECRET_KEY`, allowed host, and collected static files.

## Django Admin

After creating a superuser, open `http://127.0.0.1:8000/admin/`. The admin interface registers `Package` and `Booking`; access requires staff/admin credentials.

## Tests and verification

Run the following commands from the project root after setup:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test bookings
```

The tests cover blocking direct access to the success page without a successful booking, the valid booking submission/success flow, repeatable demo-package loading, the empty-package state, rejection of an invalid phone number, the custom 404 handler with debug disabled, and the theme cookie redirect. The valid-booking test deliberately checks the initial redirect without following it, because following it consumes the one-time success session flag before the test can assert the success page itself.

Record the actual outcomes in `Documentation/Verification_Record.md`. Do not mark a command as passing unless its output confirms success.

## Migrations

Keep all files in `bookings/migrations/` in version control. The migrations create the models, update the event type choices, allow a blank email, and add database check constraints for package price, duration, and photo count.

## Known limitations

- The form creates a booking request with status `Pending`; it does not automatically confirm availability or prevent two requests for the same date/time.
- There is no payment processing or customer account system.
- Phone-format and future-date rules are enforced in the Django form, not as database constraints; direct ORM/database writes can bypass form-only validation.
- The branded 404 page is served only when `DEBUG=False`; Django's technical 404 page is expected during ordinary development with `DEBUG=True`. Follow the README's 404 verification steps to test the branded page with collected static files.
- If no package records exist, the booking page displays an empty-state message and disables the booking submit button until packages are added in Django Admin.

## Future improvements

Potential future work, not current functionality:

- Add an availability workflow that checks date/time conflicts before a request can be confirmed.
- Add automated tests for invalid form submissions and model constraints.
- Improve deployment configuration and production secret management.
- Add a staff workflow for contacting customers and confirming or cancelling requests.

## Design system

| Color | Hex |
|---|---|
| Walnut Wood | `#6B4A33` |
| Grey / Taupe | `#A6A39D` |
| Milky White / Soft White | `#F4EFEA` |

## Author

Taif Alosaimi — Full-Stack Developer in training.

## Project Purpose

DST Photobooth is an Arabic-first photobooth booking website built with Django. It allows customers to explore the business, view available packages, and submit booking requests through an online form.

This is an educational and portfolio project.
