"""
WSGI config for ai_powered_blog project.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

base_dir = Path(__file__).resolve().parent.parent.parent
env_file = base_dir / ".env"
if env_file.exists():
    load_dotenv(env_file)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "ai_powered_blog.settings.prod",
)

application = get_wsgi_application()
