from dcim.models.cables import Cable
from extras.plugins.utils import get_plugin_config
from jinja2 import Environment, BaseLoader


def render_label(cable: Cable):
    """Render a cable label using the configured template."""
    label_template = get_plugin_config("auto_cable_label", "label_template")
    env = Environment(loader=BaseLoader)  # type: ignore
    template = env.from_string(label_template)
    return template.render(cable=cable)
