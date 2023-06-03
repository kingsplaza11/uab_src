from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!x8%r#zmlfmqu2vwb78&*seglb0$x1^%p#xzz(k^c1^$h15l+$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'account',
    'bank',
    'main',
    'site_admin',
    'crispy_forms',
]

AUTH_USER_MODEL = 'account.Account'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uab_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'uab_proj.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# media path settings
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


# authentication & access control
LOGIN_URL = 'login-view'
LOGIN_REDIRECT_URL = 'user-dashboard'
LOGOUT_REDIRECT_URL = 'login-view'


# settings.py


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'mtbauthuser@gmail.com'
EMAIL_HOST_PASSWORD = 'brwmubdjxdjbghsx'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'noreply@mbtsavings.com'
# SMTP Configuration for Gmail
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'agbanking06@gmail.com'  # Replace with your email address
# EMAIL_HOST_PASSWORD = 'kfheidzmuixupwpe'  # Replace with your email password
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = True

# Default Sender
# DEFAULT_FROM_EMAIL = 'noreply@mbtsavings.com'  # Replace with your desired no-reply email address



# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
