"""
NetBox test configuration for netbox-cable-labels plugin
"""

ALLOWED_HOSTS = ["*"]

DATABASE = {
    "NAME": "netbox",  # Database name
    "USER": "netbox",  # PostgreSQL username
    "PASSWORD": "netbox",  # PostgreSQL password
    "HOST": "localhost",  # Database server
    "PORT": "",  # Database port (leave blank for default)
    "CONN_MAX_AGE": 300,  # Max database connection age
}

REDIS = {
    "tasks": {
        "HOST": "localhost",
        "PORT": 6379,
        "PASSWORD": "",
        "DATABASE": 0,
        "SSL": False,
    },
    "caching": {
        "HOST": "localhost",
        "PORT": 6379,
        "PASSWORD": "",
        "DATABASE": 1,
        "SSL": False,
    },
}

SECRET_KEY = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz0123456789"

PLUGINS = [
    "netbox_cable_labels",
]

PLUGINS_CONFIG = {"netbox_cable_labels": {"label_template": "#{{cable.pk}}"}}
