from pathlib import Path
import environ
from datetime import timedelta

env = environ.Env(
#deixamos False por padrão caso o .env não defina, por segurança, é melhor, já que o ambiente pode ser o de produção
DEBUG = (bool, False)
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / Path(".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ["*","http://localhost:61371","http://localhost:61371/#/","http://localhost:49534/#/"]

CORS_TRUSTED_ORIGINS = ["*","http://localhost:61371","http://localhost:61371/#/","http://localhost:49534/#/"]

CSRF_COOKIE_SECURE = False
  
CSRF_TRUSTED_ORIGINS = ['http://localhost:61371',"http://localhost:49534/#/"]  

CORS_ALLOW_ALL_ORIGINS = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'dados',
    'environ',
    'corsheaders',
    'requests'
]
SIMPLE_JWT = {
    'ACESS_TOKEN_LIFETIME': timedelta(minutes=60),#tempo que dura o token
    'REFRESH_TOKEN_LIFETIME':timedelta(days=1),#tempo que o refresh do token vai durar
    'ROTATE_REFRESH_TOKENS':False,#se o refresh token vai ser rotacionado
    'ALGORITHM':'HS256',#algortimo de criptografia
    'SIGNING_KEY': env('SECRET_KEY'),#chave de criptografia
    'AUTH_HEADER_TYPES': ('Bearer'),#tipo de autenticação
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.common.CommonMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'dados.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'dados.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_DEFAULT_NAME'),
        'USER': env('DATABASE_DEFAULT_USER'),
        'PASSWORD': env('DATABASE_DEFAULT_PASSWORD'),
        'HOST': env('DATABASE_DEFAULT_HOST'),
        'PORT': env('DATABASE_DEFAULT_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'cicddronestest@gmail.com'
EMAIL_HOST_PASSWORD = 'erevbcjqzrxqczsh'

