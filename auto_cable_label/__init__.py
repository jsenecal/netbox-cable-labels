from extras.plugins import PluginConfig


class AutoCableLabelConfig(PluginConfig):
    name = "auto_cable_label"
    verbose_name = "Auto Cable Label"
    description="Plugin for NetBox that automatically adds labels to cables based on the ANSI/TIA-606 Standards",
    author_email="contact@jonathansenecal.com",
    author = "Jonathan Senecal"
    version = "0.1"
    base_url = "autocablelabel"
    min_version = "3.3"

config = AutoCableLabelConfig
