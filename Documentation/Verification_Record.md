# Verification Record — DST Photobooth

Use this record against the exact project version prepared for submission. Mark a scenario **PASS** only after running it and observing the expected result. Record any mismatch in the Actual result column and fix it before the final demo.

| Scenario | Expected result | Actual result | Status |
|---|---|---|---|
| Fresh setup: migrations on a clean local database | Migrations complete without errors | `python manage.py migrate --noinput` completed successfully in an isolated clean copy | PASS |
| Static files: `python manage.py collectstatic --noinput` | Static files collect without errors so WhiteNoise can serve them with `DEBUG=False` | 144 files copied and 688 post-processed successfully | PASS |
| Demo package setup: `python manage.py load_demo_packages` | Creates the three approved packages on a fresh database; a second run does not duplicate them | First run created 3 packages; second run skipped all 3; package count remained 3 | PASS |
| Django configuration check: `python manage.py check` | Django reports no issues | `System check identified no issues (0 silenced).` | PASS |
| Migration consistency: `python manage.py makemigrations --check --dry-run` | No ungenerated model changes are reported | `No changes detected` | PASS |
| Automated booking tests: `python manage.py test bookings` | All booking, validation, seed-command, 404, and theme tests pass | `Ran 7 tests`; `OK` | PASS |
| Valid booking submission | A valid booking is saved once with status `Pending`, then the success page is available on the next request | Automated test passes; the initial redirect is asserted without following it, so the one-time session flag remains available for the explicit success-page assertion | PASS |
| Direct/repeated success-page access | Without the one-time session flag, the visitor is redirected to the booking form | Covered by the passing automated test suite | PASS |
| Invalid phone number | The form is re-rendered with a validation message and no booking is saved | Covered by the passing automated test suite; no booking is saved | PASS |
| Unknown URL with `DEBUG=False` | Custom Arabic 404 page renders and the response status is `404` | Test returned `404` and matched the current Arabic page text; live isolated-server request also returned `404` | PASS |
| Static files for booking and branded 404 pages | Their hashed CSS assets load successfully with `DEBUG=False` | Live isolated-server requests for booking CSS and 404 CSS returned `200` | PASS |
| Unknown URL with `DEBUG=True` | Django's technical development 404 page is expected | Expected Django development behavior; not a production-page test | Informational |
| Booking page with no package records | A clear empty-state message appears and the submit button is disabled | Covered by the passing automated test suite | PASS |
| Theme selection | The theme cookie is set and the visitor returns to a safe requested URL | Covered by the passing automated test suite | PASS |
| Responsive layout | Home, About, booking, success, and 404 pages remain usable on mobile and desktop | Must be checked in a browser at narrow and wide viewport sizes | Pending manual verification |

**Test environment note:** Automated checks above were run against this revised source copy in an isolated environment with Django 6.1.1. Re-run the documented commands in the local environment used for submission before pushing the final commit.

## Known limitations to retain in the demo explanation

- A submitted form creates a booking request with `Pending` status; it does not automatically confirm availability.
- The current project does not include payment processing, customer accounts, or automatic double-booking prevention.
- The branded 404 page is expected only when `DEBUG=False`; the technical 404 page is normal during development with `DEBUG=True`.

## Final sign-off

Before submission, follow the complete setup in `README.md` from a clean database, rerun `check`, `makemigrations --check --dry-run`, and `test bookings` in the submission environment, complete the pending responsive-layout check, and update this record if the observed outcomes differ. Do not mark unexecuted checks as passed.
