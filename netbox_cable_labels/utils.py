from dcim.models.cables import Cable

try:
    from netbox.plugins.utils import get_plugin_config
except ImportError:
    from netbox.plugins import get_plugin_config  # type: ignore
from jinja2 import Environment, BaseLoader


def render_label(cable: Cable):
    """Render a cable label using the configured template."""
    label_template = get_plugin_config("netbox_cable_labels", "label_template")
    env = Environment(loader=BaseLoader)  # type: ignore
    template = env.from_string(label_template)
    return template.render(cable=cable)
