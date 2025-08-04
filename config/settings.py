from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-nj@98an)21aj!w7&ky0=f(5w+&xh)s_9&vi8blme3uhtje)8^+'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'apps.usuarios', 
    'apps.pacientes',
    'apps.reportes',
    'apps.productos',
    'apps.categorias',
    'apps.web'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False

CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'https://optica.up.railway.app']

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'qHNhaCYDwhkwUWzJAmjdcgbTKLmOGsQp',
        'HOST': 'yamanote.proxy.rlwy.net',  
        'PORT': '22075',      
    }
}

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

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/La_Paz'

USE_I18N = True

USE_TZ = True

LOGIN_URL = 'login'  
LOGOUT_REDIRECT_URL = 'login'  
AUTH_USER_MODEL = 'usuarios.Usuario'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

'''
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
'''

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

COMPRESS_ROOT = BASE_DIR / 'static'

COMPRESS_ENABLED = True

STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
CLOUDFLARE_R2_ACCESS_KEY = '19e4178c6ebc64761440e0c8f0e6a43c'
CLOUDFLARE_R2_SECRET_KEY  = '1761a98a11ef89e01d37fae4f8032a734b491e8e30a93bbe78d5b62ecfa36b80'
CLOUDFLARE_R2_BUCKET = 'caterbot-bucket'
CLOUDFLARE_R2_BUCKET_ENDPOINT = 'https://dea18ceb8496cd48c6b923cf46ee24dc.r2.cloudflarestorage.com'



