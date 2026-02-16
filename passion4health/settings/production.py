from .base import *

DEBUG = False
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-j&!)*jv%m61)_zzx*k9%c(q32res)m_*&@#*ox779%kn8n^7j7"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["localhost", "www.passion4health.org", "passion4health.org"]
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# This should be the directory where static files are collected
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

try:
    from .local import *
except ImportError:
    pass
