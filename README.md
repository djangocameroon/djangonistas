# Djangonista

A lightweight Django + Tailwind (CDN) starter crafted for Hacktoberfest 2025 with the Django Cameroon community.

## Highlights

- Uses `uv` for blazing-fast dependency management.
- Tailwind CSS via CDN with sleek directory and detail pages.
- JSON-powered data that seeds the database via focused management commands.
- Ready-to-run Django admin and tests for quick local verification.

## Quick Start

```bash
# Install dependencies
uv sync

# Apply migrations and load JSON-backed sample data
uv run python manage.py migrate
uv run python manage.py seed_people --refresh
uv run python manage.py seed_communities --refresh
uv run python manage.py seed_schools --refresh

# Launch the development server
uv run python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the landing page, `/people/`, `/communities/`, and `/schools/` for paginated directories, or append a slug (e.g. `/people/yokwe-juste/`) for individual profiles.

## Project Layout

```
.
├── data/                 # JSON data consumed by the landing page
├── djangonista/          # Django project configuration
├── hub/                  # App with views, templates, models, and seed commands
├── manage.py
├── pyproject.toml        # Managed by uv
└── uv.lock
```

Update the JSON files in `data/` to showcase new contributors, partner communities, or schools.

## Contributing

We welcome contributions from first-time and seasoned contributors alike. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for detailed guidelines, workflows, and testing tips.

## License

This project is released under the [MIT License](LICENSE).
