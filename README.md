# Stuff for Friends

A cozy lending library for sharing your stuff with friends. List your books, games, tools, and treasures - then share a private link so friends can browse and request to borrow.

## Features

- **Personal Library**: Catalog items with images, descriptions, and borrow time limits
- **Private Lending Links**: Each user gets a unique URL to share with friends
- **Borrow Workflow**: Request → Approve → Lent Out → Returned
- **Privacy Controls**: Choose what friends can see (borrowed items, borrower names, history)
- **No Friend Accounts Needed**: Friends just enter their name - it's honor-based for real-life friendships

## Tech Stack

- Django 5.1 + HTMX
- PostgreSQL
- WhiteNoise for static files
- Cropper.js for image cropping
- Custom CSS (no frameworks)

## Development Setup

```bash
# Start PostgreSQL
docker compose up -d

# Set up Python environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python manage.py migrate

# Create root admin user
export ROOT_USERNAME=admin ROOT_PASSWORD=your-secure-password
python manage.py ensure_root_user

# Run development server
python manage.py runserver
```

Visit http://localhost:8000 to see the app.

## Production Deployment

```bash
# Build and run with Docker Compose
docker compose -f docker-compose.prod.yml up -d
```

Required environment variables for production:
- `SECRET_KEY` - Django secret key
- `POSTGRES_PASSWORD` - Database password
- `ROOT_PASSWORD` - Admin user password
- `ALLOWED_HOSTS` - Your domain
- `CSRF_TRUSTED_ORIGINS` - Your domain with https://

## User Workflow

1. **Admin** approves new user registrations via Django admin (`/admin/`)
2. **User** adds items to their library with optional images
3. **User** shares their lending link (e.g., `yoursite.com/lend/abc123/`)
4. **Friend** visits the link, enters their name, and requests items
5. **User** approves/denies requests from their dashboard
6. **User** marks items as "lent out" when handed over
7. **User** marks items as "returned" when they come back

## License

See LICENSE file.
