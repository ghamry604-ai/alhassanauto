import os
from django.core.wsgi import get_wsgi_application  # type: ignore[import]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carsite.settings')
application = get_wsgi_application()
app = application
