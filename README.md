# Brückentech Django Project

This is a simple Django site for the Brückentech Foundation.

## Setup

1. Create a Python virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` in the project root with your environment variables. At
   minimum during development you can include:
   ```ini
   SECRET_KEY=your-secret-key
   DEBUG=True
   BANK_NAME=Example Bank
   BANK_ACCOUNT_NAME=Brückentech Foundation
   BANK_ACCOUNT_NUMBER=0000000000
   MM_PROVIDER=MTN Mobile Money
   MM_NUMBER=+256700000000
   MM_ACCOUNT_NAME=Brückentech Foundation
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. (Optional) Create a superuser to access the admin:
   ```bash
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

Visit <http://localhost:8000/> to see the site and <http://localhost:8000/admin/>
for the admin interface where you can add `Article` entries.

## Media and Production Notes

- Uploaded images are stored under `MEDIA_ROOT`. In development, the server
  serves these automatically when `DEBUG=True`.
- **Production** should use a shared storage backend (S3, Cloud Storage, etc.)
  configured via `DEFAULT_FILE_STORAGE`. See
  `django-storages` documentation for details.

  To enable S3 you'll need additional environment variables (see below).

- Account details for offline donations are read from environment variables
  (`BANK_*`, `MM_*`). The application will fail to start if any of these are
  missing when `DEBUG=False`.


### Using S3

The project can switch to Amazon S3 for media files by enabling an
environment variable and supplying AWS credentials.

```ini
USE_S3=True            # enable S3 storage when DEBUG=False
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1        # optional
AWS_S3_CUSTOM_DOMAIN=cdn.example.com  # optional
```

When `USE_S3` is truthy and `DEBUG=False`, `django-storages` is added
and `DEFAULT_FILE_STORAGE` is set appropriately.  The application will
raise an error during startup if any of the required AWS variables are
missing.

## Optional Enhancements

- Install `django-markdownx` (already added to requirements) to provide a
  rich Markdown editor and image upload support in the admin. Files are
  handled by the same storage configuration used for article images.
- Add search, pagination, and an RSS feed are already implemented.
- Remove the old `Donation` model/table if no longer needed by creating a
  migration to drop it or by manual SQL.

- The site now supports light/dark colour schemes. Users can switch using
  the moon/sun icon in the top navigation; preference is saved in
  `localStorage` and the initial theme respects the system setting.  Colours
  are configured via Tailwind and a small custom CSS file (`main.css`).

---

This README is kept deliberately small; expand as your project grows.

## Production Checklist

Before deploying to production, complete the following checks:

- **Replace placeholders**: copy `.env.example` to `.env` and replace `SECRET_KEY`, `BANK_*`, `MM_*`, and any AWS variables with real values.
- **Enable S3 (optional)**: if you plan to use S3 for media, set `USE_S3=True` and provide `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_STORAGE_BUCKET_NAME`.
- **Re-enable account validation**: open `bruckentech/settings.py` and uncomment the validation block under `ACCOUNT_DETAILS` to enforce presence of account variables when `DEBUG=False`.
- **Set production settings**: set `DEBUG=False` and configure `ALLOWED_HOSTS` appropriately.
- **Run migrations and create admin**: run `python manage.py migrate` and create a superuser with `python manage.py createsuperuser`.
- **Test media access**: upload an image in admin and verify media is served (locally with `DEBUG=True` or via S3 in production).

When these steps are complete the site will start in production without placeholder account details.