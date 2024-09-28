from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-j&!)*jv%m61)_zzx*k9%c(q32res)m_*&@#*ox779%kn8n^7j7"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]


try:
    from .local import *
except ImportError:
    pass
