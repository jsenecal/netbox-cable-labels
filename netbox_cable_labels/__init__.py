"""Top-level package for netbox_cable_labels."""

__author__ = "Jonathan Senecal"
__email__ = "contact@jonathansenecal.com"
__version__ = "0.0.3"


from extras.plugins import PluginConfig


class AutoCableLabelsConfig(PluginConfig):
    """Plugin configuration for the netbox_cable_labels plugin."""

    name = "netbox_cable_labels"
    verbose_name = "Automatic Cable Labels"
    description = "Plugin for NetBox that automatically adds labels to cables based on a customizable template."
    author_email = "contact@jonathansenecal.com"
    author = "Jonathan Senecal"
    version = __version__
    min_version = "3.5.0"
    default_settings = {"label_template": "#{{cable.pk}}"}

    def ready(self):
        super().ready()
        from . import signals  # pylint: disable=unused-import,import-outside-toplevel


config = AutoCableLabelsConfig  # pylint: disable=invalid-name

print("netbox_cable_labels plugin loaded.")
