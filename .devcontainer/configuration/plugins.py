"""
Plugin related config
"""

PLUGINS = [
    "netbox_cable_labels",
]

PLUGINS_CONFIG = {  # type: ignore
    "netbox_cable_labels": {
        # Default template (TIA-606-C compliant)
        "label_template": "{{cable.a_terminations.first().device.rack.name if cable.a_terminations.first() and cable.a_terminations.first().device and cable.a_terminations.first().device.rack else 'A'}}-{{cable.a_terminations.first().device.position if cable.a_terminations.first() and cable.a_terminations.first().device else '00'}}{{cable.a_terminations.first().device.face|first|upper if cable.a_terminations.first() and cable.a_terminations.first().device and cable.a_terminations.first().device.face else 'U'}}/{{cable.b_terminations.first().device.rack.name if cable.b_terminations.first() and cable.b_terminations.first().device and cable.b_terminations.first().device.rack else 'B'}}-{{cable.b_terminations.first().device.position if cable.b_terminations.first() and cable.b_terminations.first().device else '00'}}{{cable.b_terminations.first().device.face|first|upper if cable.b_terminations.first() and cable.b_terminations.first().device and cable.b_terminations.first().device.face else 'U'}}/{{cable.type|default('CAT6')}}/C{{'{:05d}'.format(cable.pk)}}",
    },
}
