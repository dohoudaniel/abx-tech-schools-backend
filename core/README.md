# Core Configuration

The `core` directory contains the project-wide settings and configuration for the LMS backend.

## Contents
- `settings.py`: Main configuration file (Database, Installed Apps, Middleware, DRF, JWT, Swagger).
- `urls.py`: Main routing table that aggregates URLs from all apps.
- `wsgi.py` / `asgi.py`: Entry points for web server deployments.

## Key Configurations
- **Database**: Uses `dj-database-url` to support Supabase/PostgreSQL.
- **Security**: Admin panel is disabled when `DEBUG=False`.
- **CORS**: Configured to allow interactions from the future frontend.
- **Documentation**: Houses the `drf-spectacular` settings for Swagger UI.
