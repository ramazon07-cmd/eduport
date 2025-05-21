import os
from django.core.asgi import get_asgi_application
from django.core.management import execute_from_command_line

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

if __name__ == "__main__":
    execute_from_command_line()
else:
    # Vercel expects an `app` callable
    app = get_asgi_application()