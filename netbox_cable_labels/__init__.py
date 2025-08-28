"""Top-level package for netbox_cable_labels."""

__author__ = "Jonathan Senecal"
__email__ = "contact@jonathansenecal.com"
__version__ = "0.1.0"

from netbox.plugins import PluginConfig


class AutoCableLabelsConfig(PluginConfig):
    """Plugin configuration for the netbox_cable_labels plugin.

    This plugin automatically adds labels to cables based on user-defined templates.
    """

    # Plugin metadata
    name = "netbox_cable_labels"
    verbose_name = "Automatic Cable Labels"
    version = __version__
    author = __author__
    author_email = __email__
    description = "Plugin for NetBox that automatically adds labels to cables based on a user defined template"

    # Plugin requirements
    min_version = "4.2.0"
    max_version = "4.99.99"

    # Plugin URL configuration
    base_url = "cable-labels"

    # Plugin settings
    required_settings = []
    default_settings = {"label_template": "#{{cable.pk}}"}

    def ready(self):
        """Perform plugin initialization tasks when Django is ready."""
        super().ready()
        # Import signals to register them
        from netbox_cable_labels import signals  # pylint: disable=unused-import,import-outside-toplevel


config = AutoCableLabelsConfig
