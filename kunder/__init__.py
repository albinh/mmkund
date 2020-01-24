
import os

from django.core.wsgi import get_wsgi_application
import sys
if "testlauncher" in sys.argv[0]:

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmkund.settings")

    application = get_wsgi_application()
