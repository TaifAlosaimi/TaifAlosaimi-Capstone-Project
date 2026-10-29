# Sample Data Guide — DST Photobooth

Use fictional data only in development and demos. Do not enter real customers' phone numbers, email addresses, or private event details into a public demo repository.

## 1. Load the approved package records

After applying migrations, run this command from the project root:

```powershell
python manage.py load_demo_packages
```

The command adds any of the three approved packages that are missing by name and skips existing records. It does not overwrite package details already present in the database. Running it more than once does not create duplicate demo records.

The packages use the current approved values:

| Package | Price (SAR) | Duration | Printed photos | Extra photos |
|---|---:|---:|---:|---:|
| باقة 100 صورة | 2400 | 4 hours | 100 | 10 |
| باقة 70 صورة | 1750 | 3 hours | 70 | 0 |
| باقة 50 صورة | 1300 | 2 hours | 50 | 0 |

To manage or inspect packages manually, create a superuser, open `/admin/`, and use **Packages**. Do not create invented customer-facing offers for the demo.

## 2. Create fictional booking records

Use the **Bookings** section in Django Admin to add at least five fictional records. Vary the event type and status across `Pending`, `Confirmed`, and `Cancelled`, and associate records with more than one package. Use future event dates and clearly fictional contact details. Keep at least two bookings `Confirmed` so the confirmed-booking count and confirmed-booking value are non-zero.

The admin list should let you verify:

- `PackageAdmin.booking_count` counts related bookings for each package, including a zero count for a package with no bookings.
- Booking filters can narrow the list by status, event type, date, and package.
- The confirmed booking summary counts only records with status `Confirmed`.
- The confirmed booking value sums the associated package price once for each confirmed booking. If two confirmed bookings reference the same package, that package price contributes twice because the calculation is per booking record.

## 3. Verify the results

1. Count the records with status `Confirmed` in the filtered booking list and compare that number with the admin summary.
2. Add the package prices for those confirmed booking records, including repeated package prices where multiple confirmed bookings use the same package, and compare the total with the admin summary.
3. Open the package list and compare each displayed booking count with the related booking records.
4. Repeat after changing one booking status to confirm that the summary updates.

Record the observed results in `Documentation/Verification_Record.md` if these scenarios are used for the final demo. This guide describes a repeatable method; it does not claim that any sample records already exist in a fresh database.
