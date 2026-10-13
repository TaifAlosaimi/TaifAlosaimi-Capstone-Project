# DST Photobooth

An Arabic-first booking website for DST Photobooth, built with Django.

DST Photobooth is a photography and photobooth service designed to help clients explore available packages and submit booking requests for their events through a structured and responsive web experience.

---

## Overview

This project was built as a full-stack Django application, combining a custom editorial user interface with a database-driven booking system.

The website allows visitors to:

- Explore DST Photobooth
- Learn about the brand
- View available photobooth packages
- Submit an event booking request
- Provide event and contact details
- Receive a booking confirmation page after successful submission

The project also includes a Django admin interface for managing booking-related data.

---

## Features

### User Experience

- Arabic-first interface with selected English editorial elements
- Responsive design for desktop, tablet, and mobile screens
- Premium editorial visual direction
- Custom typography and branded visual system
- Responsive navigation
- Reusable footer component
- Booking call-to-action throughout the website

### Booking System

- Package selection through the booking form
- Event type selection
- Event date selection
- Event location
- Customer name
- Phone number
- Optional email address
- Additional notes
- Django form validation
- CSRF protection
- Successful booking submission flow
- Dedicated booking success page

### Admin Management

The project uses Django Admin to manage the application's database records.

Administrators can manage:

- Photobooth packages
- Booking records
- Booking status
- Customer and event information

---


### Shared Templates and Themes

- Pages extend `bookings/base.html` to reuse the document structure and page-style block.
- The shared footer is stored in `bookings/templates/bookings/partials/footer.html`.
- Visitors can select a light or dark theme. The selection is stored in the `dst_theme` cookie for 30 days.
- The theme defaults to light when the cookie is missing or contains an unsupported value.
- Shared theme styling is defined in `bookings/static/bookings/themes.css`.

## Booking Flow

The booking process follows a simple Django request-response flow:

1. The visitor opens the booking page.
2. Available packages are loaded from the database.
3. The visitor selects a package and enters event details.
4. The form is submitted using `POST`.
5. Django validates the submitted data through `BookingForm`.
6. If the form is valid, the booking is saved to the database.
7. The visitor is redirected to the booking success page.

```text
Booking Page
     ↓
BookingForm
     ↓
Validation
     ↓
Save Booking
     ↓
Redirect
     ↓
Booking Success Page
```

---

## Django Architecture

The project is structured around Django's core application architecture.

### Models

The application uses database models to represent:

- `Package` — stores available photobooth package information.
- `Booking` — stores submitted booking information.

### Forms

The booking form is implemented using Django's `ModelForm`:

```python
class BookingForm(forms.ModelForm):
```

The form connects the HTML booking interface directly to the `Booking` model and provides Django's built-in validation system.

### Views

The application includes views for:

- Home page
- About page
- Booking creation
- Booking success page

The booking view handles both `GET` and `POST` requests.

### URLs

The application uses named Django URL patterns for navigation and redirects.

Example booking routes:

```text
/booking/
/booking/success/
```

---

## Tech Stack

### Backend

- Python
- Django
- Django ORM
- SQLite

### Frontend

- HTML5
- CSS3
- Responsive Web Design
- Google Fonts

### Development Tools

- Visual Studio Code
- PowerShell
- Git
- GitHub

---

## Project Structure

```text
DST/
│
├── bookings/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── dst_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
│   └── bookings/
│
├── templates/
│   └── bookings/
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

> Local development files such as `venv/`, `db.sqlite3`, `secret_key.txt`, Python cache files, and environment files are excluded from version control.

---

## Data Models

### Package

The `Package` model represents a DST Photobooth package and stores information used to display package options in the booking form.

Package information includes:

- Package name
- Photo count
- Extra photos
- Duration
- Price
- Description

### Booking

The `Booking` model stores the information submitted by a customer.

Booking information includes:

- Customer name
- Phone number
- Email address
- Event type
- Event date
- Event location
- Selected package
- Additional notes
- Booking status

---

## Responsive Design

The interface was designed with a responsive-first mindset to provide a consistent experience across different screen sizes.

The project includes dedicated responsive styling for:

- Desktop
- Tablet
- Mobile
- Small mobile screens

The visual system focuses on maintaining the same editorial identity while adapting layouts, spacing, typography, and navigation for smaller screens.

---

## Design Direction

The website follows a premium editorial visual direction inspired by luxury print and photography layouts.

### Brand Palette

| Color | Hex |
|---|---|
| Walnut Wood | `#6B4A33` |
| Grey / Taupe | `#A6A39D` |
| Milky White | `#F4EFEA` |

The interface uses a minimal color system with typography, spacing, composition, and subtle motion as the main visual elements.

---

## Security

Sensitive development files are excluded from version control.

The project keeps the Django `SECRET_KEY` outside the source code using a local `secret_key.txt` file, which is excluded through `.gitignore`.

The following local files are also excluded:

```text
venv/
__pycache__/
*.pyc
db.sqlite3
secret_key.txt
.env
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/dst-photobooth.git
cd dst-photobooth
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Create your local secret key

Create a file named:

```text
secret_key.txt
```

in the project root.

Generate a new Django secret key with:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key into `secret_key.txt`.

> Never commit `secret_key.txt` to GitHub.

### 6. Apply migrations

```powershell
python manage.py migrate
```

### 7. Create an admin account

```powershell
python manage.py createsuperuser
```

### 8. Run the development server

```powershell
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

---

## Admin Dashboard

Django's built-in admin interface is used to manage application data.

After creating a superuser, access:

```text
http://127.0.0.1:8000/admin/
```

From the admin dashboard, authorized administrators can manage packages and booking records.

---

## Screenshots

Screenshots of the project interface will be added here.

Suggested sections:

- Home
- About
- Booking
- Booking Success
- Django Admin

---

## Project Status

This project is actively developed as a portfolio full-stack Django project.

The current version focuses on:

- Django fundamentals
- Database-driven booking functionality
- Form handling and validation
- Django Admin
- Responsive frontend development
- Clean project structure
- Secure handling of development secrets

---

## Author

### Eng. Taif Alosaimi

Physics graduate and Full-Stack Developer focused on building practical web applications using Python and Django.

This project reflects my transition into software development and my hands-on experience building full-stack applications.

---

## License

This project is created for portfolio and educational purposes.
