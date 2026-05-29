# AutoElite Car Dealership

A fully functional, production-ready car dealership web application built with Django, Bootstrap 5, and SQLite (scalable to PostgreSQL).

---

## Directory Structure

```
cardealership/
├── manage.py
├── requirements.txt
├── setup_and_run.sh
├── db.sqlite3              ← auto-created after migrate
├── media/                  ← uploaded images (auto-created)
│   └── car_images/
├── staticfiles/            ← auto-created by collectstatic
│
├── carsite/                ← Django project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── dealership/             ← Main app
    ├── __init__.py
    ├── apps.py
    ├── models.py           ← Brand, Car, CarImage
    ├── admin.py            ← Rich admin with thumbnails, filters
    ├── views.py            ← homepage, car_list, car_detail
    ├── urls.py             ← URL routing
    ├── management/
    │   └── commands/
    │       └── seed_data.py  ← Sample data seeder
    ├── templates/
    │   └── dealership/
    │       ├── base.html       ← Base layout + navbar + footer
    │       ├── home.html       ← Homepage with hero + featured cars
    │       ├── car_list.html   ← Listings with sidebar filters
    │       ├── car_detail.html ← Car detail with gallery
    │       └── _car_card.html  ← Reusable car card partial
    └── static/
        ├── css/
        │   └── style.css     ← Luxury dark theme
        └── js/
            └── main.js       ← Animations, back-to-top, scroll FX
```

---

## Quick Setup (Ubuntu/Debian)

### Prerequisites
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### Option A — Automated (recommended)
```bash
cd cardealership
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### Option B — Manual step-by-step
```bash
# 1. Navigate to project root
cd cardealership

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Seed sample data (optional but recommended)
python manage.py seed_data

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Create admin user
python manage.py createsuperuser

# 8. Start the server
python manage.py runserver
```

Then open:
- **Website**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin

---

## Pages & URLs

| URL | View | Description |
|-----|------|-------------|
| `/` | `homepage` | Hero, featured cars, latest arrivals |
| `/cars/` | `car_list` | Full inventory with filters + pagination |
| `/cars/<slug>/` | `car_detail` | Full detail page with gallery |
| `/admin/` | Django Admin | Manage all inventory |

### Filter Parameters (car_list)
- `?brand=toyota` — filter by brand slug
- `?condition=new` — new / used / certified
- `?fuel_type=electric` — petrol / diesel / electric / hybrid
- `?transmission=manual` — automatic / manual / cvt
- `?min_price=20000&max_price=50000` — price range
- `?sort=-price` — sorting (price, -price, year, -year, created_at)

---

## Admin Dashboard

Log in at `/admin/` with your superuser credentials.

Features:
- **Brands**: Create brands with logos
- **Cars**: Full CRUD with inline image upload, thumbnail preview, all filters
- **Car Images**: Bulk manage images, set main image

After seeding, you'll have 8 brands and 12 cars ready. Add images via the admin panel (Car → Inline Images section).

---

## Upgrading to PostgreSQL

1. Install psycopg2: `pip install psycopg2-binary`
2. Create a PostgreSQL database
3. In `carsite/settings.py`, replace the `DATABASES` block:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cardealership',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

4. Run `python manage.py migrate` again

---

## Production Deployment Notes

For production on Ubuntu with Nginx + Gunicorn:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn carsite.wsgi:application --bind 0.0.0.0:8000 --workers 3

# Update settings.py for production:
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = 'use-a-real-secret-key-from-env'

# Use whitenoise for static files (add to requirements.txt):
pip install whitenoise
# Add to MIDDLEWARE (after SecurityMiddleware):
# 'whitenoise.middleware.WhiteNoiseMiddleware',
```

---

## Tech Stack

- **Backend**: Django 4.2 (Python)
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: HTML5, CSS3, Bootstrap 5.3
- **Fonts**: Playfair Display + DM Sans (Google Fonts)
- **Icons**: Bootstrap Icons 1.11
- **Image handling**: Pillow
