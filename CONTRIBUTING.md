# Contributing to Djangonista

Thanks for supporting Django Cameroon and Hacktoberfest 2025! This project keeps the barrier to entry low so newcomers can focus on learning and making their first pull request.

## Quick Start

1. **Install Python 3.11+** (or let `uv` manage it).
2. **Install dependencies**:
   ```bash
   uv sync
   ```
3. **Run migrations and seed starter data** (use `--refresh` to wipe existing rows first):
   ```bash
   uv run python manage.py migrate
   uv run python manage.py seed_people --refresh
   uv run python manage.py seed_communities --refresh
   uv run python manage.py seed_schools --refresh
   ```
4. **Start the development server**:
   ```bash
   uv run python manage.py runserver
   ```
5. Visit `http://127.0.0.1:8000/` to explore the Tailwind-powered hub.

## Making Changes

- Leave a star ⭐ to the repository
- Create a feature branch: `git checkout -b feature/your-idea`.
- Keep commits focused; small changes are easier to review.
- Update or add tests when behaviour changes.
- Run quality checks before submitting:
  ```bash
  uv run python manage.py check
  uv run python manage.py test
  ```

## Data Updates

Community partners, people, and schools live in JSON files under `data/`. After editing those files, run the matching seed command (`seed_people`, `seed_communities`, or `seed_schools`) so the database stays in sync. If you remove or rename fields, update `hub/models.py`, views, and templates to match.

## Pull Requests

- Fill in the pull request template so maintainers understand the impact.
- Link to related issues with `Closes #123` where possible.
- Screenshots or screen recordings help us verify UI changes quickly.

## Code of Conduct

We follow the [Django Code of Conduct](https://www.djangoproject.com/conduct/). Be kind, inclusive, and respectful in all interactions.

Happy hacking! ✨
