# -*- coding: utf-8 -*-
import os
from lms.envs.devstack import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "connect": False,
    "ssl": False,
    "authsource": "admin",
    "replicaSet": None,
    
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Meilisearch connection parameters
MEILISEARCH_ENABLED = True
MEILISEARCH_URL = "http://meilisearch:7700"
MEILISEARCH_PUBLIC_URL = "https://meilisearch.institute.airoboticx.com"
MEILISEARCH_INDEX_PREFIX = "tutor_"
MEILISEARCH_API_KEY = "caaa4f7c50d0d873a8baee28d86172695306d9dc381d68f606df1de53aaf5556"
MEILISEARCH_MASTER_KEY = "lFhOmIWsql6yMnUiJSxrqoCd"
SEARCH_ENGINE = "search.meilisearch.MeilisearchEngine"

# Common cache config
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 604800, # 1 week
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "ora2-storage": {
        "KEY_PREFIX": "ora2-storage",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    }
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "Astute Institue of AI & Robotics - https://institute.airoboticx.com"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

# ORA2
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]

# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)
LOGGING["loggers"]["blockstore.apps.bundles.storage"] = {"handlers": ["console"], "level": "WARNING"}

# These warnings are visible in simple commands and init tasks
import warnings

# REMOVE-AFTER-V20: check if we can remove these lines after upgrade.
from django.utils.deprecation import RemovedInDjango50Warning, RemovedInDjango51Warning
# RemovedInDjango5xWarning: 'xxx' is deprecated. Use 'yyy' in 'zzz' instead.
warnings.filterwarnings("ignore", category=RemovedInDjango50Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango51Warning)
# DeprecationWarning: 'imghdr' is deprecated and slated for removal in Python 3.13
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pgpy.constants")

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "https://institute.airoboticx.com/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "B9EI15v07uIFAVP5to6VX7Vx"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "FFuxBr0yk7qK69KiuoNfXd0kyLXFFY7aUsB1Yu3yQbdBSpGDHCH3BC4q3pYeHGiIEkSp8bHI2I4QEKKQE8X9yRZIfD4rMPcOJLnnNNfI2s7t_a9HTHKWl3_7HR8-3xhmiKopcUKyZkVhWIVMot3P3-uPs0Sx-zkwYA4CQG08kj24WjzXp_C18jJq_RYgfSDLWSUNayCrojws2G22sRByBhPJVQWhJ4e_k_xEJ5VaFAMcHJt2BuldhjgoBrDE5f9tF1kopJlz-N7rzRgOqjI_shWk0Ah5szoDdEWHBXEh3zCzVU1XnNXhDUIKH80-0plHXCBHfE7hoMngo1cKHUBMdw",
        "n": "jnSUDKcBrdIkqgBoJ0WQk8vm7BNPWm5JeHBKEzJ3kwkm_tCSg_e42JXxeFpmx2DSzHuk01pD3CCB2km4Kvz6CfXY_cygBb8rDHXza3FZDgL2-Vey4DsfimQVlksaVf-Px60AInGiQ4joNB116DkcUIuSeG7Aq72ITfvKOEP1ugNSQW94GIZyi0__jYpt617eKmqKJd67yiGfhSjTyp3-lAG9iK647nGe-9z39u7hoGiGmJRYkVeo2iicuYQq3MouvskAKZhQ00abKRkBc-aokaVPxmbExy12AM9NZP2hknC0Op7j5W9C-cdV1FQb6RZGt_e4CG6ji1pLWILgtqu7lQ",
        "p": "vZz1LOoOIq98-Psv1ZJeCV9_9dyPYxMJv2iWJyK5NKwG9bbHaGU5u6vGhB5M75lNX7LHMmLyBOAMWxTavE2-zNk8GwxjHHTVbWbgUf7re44JQAhy4zoONy4-35fBAA_gQ_1iJxzL4_8cSSU7WCSdB2pcpz4eyZzO4hXwPOJr9e8",
        "q": "wFTeUY5fcREVJQaJLs1KPFZ3Ejcq0UM6STXReo4kU8sck4JRovzEsWVLJuuluN0aaRoxZAR09nCErCESIUesM1clSuRcYWaj9sudQ-N5ZTF-PAWV6oirg_MyObkrgKRT_XBa4koW3xBzTBVkFmxhP-u2QTRWVL_w5JiWDabISrs",
        "dq": "iRy3tUqbTd7QxSmIqN3fW26Eym6bzr1vkvuUEBu_WCFHiP1xt5EdpB3DWsbJySWPC3iJ13S58Wo7mv6kjycqYxtwUZjFJwbmQy3bOqezRmnnRWDyBFZUd-frWW1hzv7XhakQkZwh-_odSBND3Bx9o_UlZAyssxR25nDFIIxS47s",
        "dp": "F23nla8uI_cPOCzBkmBNolbcluK0DQfzMmWX-CoAPJPtIDt_lFS9t4TYOMcNtqV4vBR5LK6xPQz6Od7v0EjDBMjq9mSncoK1RJlrqnYXXuMEHZdtqsonq4XZWwODY6CSk5QhpreWMgv50Mf69z8-8AWigT_ZygvIPIN9deh8cp0",
        "qi": "HSiP0g10Ste2IT3FZqlhcc1WQ6eBS41ZEg8bSqQ2SoZ6godkDRUHtqNsiS4BnNFeJfHd3eiq-zJvMWy5eZQo5rGA2vx5rh7N2qGTJEkWGCQYFRdzScRDLu_0jvyAbA1LrySUu8zGRuyWP_zeKclmjr-5FcCmjGmX6Rx2p-nsPFY",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "jnSUDKcBrdIkqgBoJ0WQk8vm7BNPWm5JeHBKEzJ3kwkm_tCSg_e42JXxeFpmx2DSzHuk01pD3CCB2km4Kvz6CfXY_cygBb8rDHXza3FZDgL2-Vey4DsfimQVlksaVf-Px60AInGiQ4joNB116DkcUIuSeG7Aq72ITfvKOEP1ugNSQW94GIZyi0__jYpt617eKmqKJd67yiGfhSjTyp3-lAG9iK647nGe-9z39u7hoGiGmJRYkVeo2iicuYQq3MouvskAKZhQ00abKRkBc-aokaVPxmbExy12AM9NZP2hknC0Op7j5W9C-cdV1FQb6RZGt_e4CG6ji1pLWILgtqu7lQ",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "https://institute.airoboticx.com/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "B9EI15v07uIFAVP5to6VX7Vx"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = False
# Note: CORS_ALLOW_HEADERS is intentionally not defined here, because it should
# be consistent across deployments, and is therefore set in edx-platform.

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}

OPENEDX_LEARNING = {
    'MEDIA': {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": "/openedx/media-private/openedx-learning",
        }
    }
}


######## End of settings common to LMS and CMS

######## Common LMS settings
LOGIN_REDIRECT_WHITELIST = ["studio.institute.airoboticx.com"]

# Better layout of honor code/tos links during registration
REGISTRATION_EXTRA_FIELDS["terms_of_service"] = "hidden"
REGISTRATION_EXTRA_FIELDS["honor_code"] = "hidden"

# Fix media files paths
PROFILE_IMAGE_BACKEND["options"]["location"] = os.path.join(
    MEDIA_ROOT, "profile-images/"
)

COURSE_CATALOG_VISIBILITY_PERMISSION = "see_in_catalog"
COURSE_ABOUT_VISIBILITY_PERMISSION = "see_about_page"

# Allow insecure oauth2 for local interaction with local containers
OAUTH_ENFORCE_SECURE = False

# Email settings
DEFAULT_EMAIL_LOGO_URL = LMS_ROOT_URL + "/theming/asset/images/logo.png"
BULK_EMAIL_SEND_USING_EDX_ACE = True
FEATURES["ENABLE_FOOTER_MOBILE_APP_LINKS"] = False

# Branding
MOBILE_STORE_ACE_URLS = {}
SOCIAL_MEDIA_FOOTER_ACE_URLS = {}

# Make it possible to hide courses by default from the studio
SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING = False

# Caching
CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_lms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_lms",
}

# Enable search features
FEATURES["ENABLE_COURSE_DISCOVERY"] = True
FEATURES["ENABLE_COURSEWARE_SEARCH"] = True
FEATURES["ENABLE_DASHBOARD_SEARCH"] = True

# Create folders if necessary
for folder in [DATA_DIR, LOG_DIR, MEDIA_ROOT, STATIC_ROOT, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)



######## End of common LMS settings

# Setup correct webpack configuration file for development
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"

LMS_BASE = "institute.airoboticx.com:8000"
LMS_ROOT_URL = "http://{}".format(LMS_BASE)
LMS_INTERNAL_ROOT_URL = LMS_ROOT_URL
SITE_NAME = LMS_BASE
CMS_BASE = "studio.institute.airoboticx.com:8001"
CMS_ROOT_URL = "http://{}".format(CMS_BASE)
LOGIN_REDIRECT_WHITELIST.append(CMS_BASE)

MEILISEARCH_PUBLIC_URL = "https://meilisearch.institute.airoboticx.com:7700"

# Session cookie
SESSION_COOKIE_DOMAIN = "institute.airoboticx.com"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"

# CMS authentication
IDA_LOGOUT_URI_LIST.append("http://studio.institute.airoboticx.com:8001/logout/")

FEATURES["ENABLE_COURSEWARE_MICROFRONTEND"] = False

# Disable enterprise integration
FEATURES["ENABLE_ENTERPRISE_INTEGRATION"] = False
SYSTEM_WIDE_ROLE_CLASSES.remove("enterprise.SystemWideEnterpriseUserRoleAssignment")

LOGGING["loggers"]["oauth2_provider"] = {
    "handlers": ["console"],
    "level": "DEBUG"
}



javascript_files = ['base_application', 'application', 'certificates_wv']
dark_theme_filepath = ['indigo/js/dark-theme.js']

for filename in javascript_files:
    if filename in PIPELINE['JAVASCRIPT']:
        PIPELINE['JAVASCRIPT'][filename]['source_filenames'] += dark_theme_filepath

MFE_CONFIG['INDIGO_ENABLE_DARK_TOGGLE'] = True