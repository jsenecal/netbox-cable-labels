"""
NetBox test configuration for netbox-cable-labels plugin
"""

import os
import sys

# Database configuration for testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "netbox"),
        "USER": os.getenv("POSTGRES_USER", "netbox"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "netbox"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# Redis configuration
REDIS = {
    "tasks": {
        "HOST": os.getenv("REDIS_HOST", "localhost"),
        "PORT": int(os.getenv("REDIS_PORT", 6379)),
        "PASSWORD": os.getenv("REDIS_PASSWORD", ""),
        "DATABASE": 0,
        "SSL": os.getenv("REDIS_SSL", "False").lower() == "true",
    },
    "caching": {
        "HOST": os.getenv("REDIS_HOST", "localhost"),
        "PORT": int(os.getenv("REDIS_PORT", 6379)),
        "PASSWORD": os.getenv("REDIS_PASSWORD", ""),
        "DATABASE": 1,
        "SSL": os.getenv("REDIS_SSL", "False").lower() == "true",
    },
}

# Security settings (for testing only)
SECRET_KEY = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz0123456789"
ALLOWED_HOSTS = ["*"]

# Plugin configuration
PLUGINS = ["netbox_cable_labels"]

PLUGINS_CONFIG = {
    "netbox_cable_labels": {
        "label_template": "#{{cable.pk}}"
    }
}

# Testing mode
DEBUG = True
TESTING = True

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Media and static files
MEDIA_ROOT = "/tmp/netbox_media"
STATIC_ROOT = "/tmp/netbox_static"

# Time zone
TIME_ZONE = "UTC"

# Required NetBox settings
RQ_DEFAULT_TIMEOUT = 300
PAGINATE_COUNT = 50