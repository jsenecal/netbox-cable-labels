# Cable Label Templates

This document provides example templates for the netbox-cable-labels plugin, including TIA-606-C compliant formats.

## TIA-606-C Standard Templates

The TIA-606-C standard specifies that cable labels should include termination points and pathway information. The general format is:
**Near End - Far End / Media Type / Identifier**

### Basic TIA-606-C Template

```python
PLUGINS_CONFIG = {
    "netbox_cable_labels": {
        "label_template": "{{cable.a_terminations.first().device.site.name}}-{{cable.a_terminations.first().device.name}}/{{cable.b_terminations.first().device.site.name}}-{{cable.b_terminations.first().device.name}}/{{cable.type|default('CAT6')}}/{{cable.pk}}"
    }
}
```

### Rack-Based Template
Includes rack location and device position:

```python
PLUGINS_CONFIG = {
    "netbox_cable_labels": {
        "label_template": "{{cable.a_terminations.first().device.rack.name}}-{{cable.a_terminations.first().device.position}}{{cable.a_terminations.first().device.face|first|upper}}/{{cable.b_terminations.first().device.rack.name}}-{{cable.b_terminations.first().device.position}}{{cable.b_terminations.first().device.face|first|upper}}/{{cable.type|default('UTP')}}/C{{'{:05d}'.format(cable.pk)}}"
    }
}
```
Example output: `R1A-42F/R2B-10R/CAT6A/C00123`

### Detailed Location Template
Includes building/location, rack, and port information:

```python
PLUGINS_CONFIG = {
    "netbox_cable_labels": {
        "label_template": "{%- set a_term = cable.a_terminations.first() -%}{%- set b_term = cable.b_terminations.first() -%}{{a_term.device.site.name|upper}}-{{a_term.device.rack.name ~ ':' ~ a_term.device.name}}-{{a_term.name}}/{{b_term.device.site.name|upper}}-{{b_term.device.rack.name ~ ':' ~ b_term.device.name}}-{{b_term.name}}{%- if cable.length %}/{{cable.length}}m{% endif %}/ID{{'{:06d}'.format(cable.pk)}}"
    }
}
```
Example output: `NYC-R1A:SW01-gi1/0/1/NYC-R2B:SW02-gi1/0/1/10m/ID000123`

Note: The `~` operator is used for string concatenation in Jinja2 when special characters like `:` need to be included.

## Data Center Templates

### Simple DC Template
```python
"label_template": "{{cable.a_terminations.first().device.name}}-{{cable.a_terminations.first().name}} to {{cable.b_terminations.first().device.name}}-{{cable.b_terminations.first().name}}"
```
Example output: `SW01-eth1/1 to SW02-eth1/1`

### Patch Panel Template
```python
"label_template": "{% set a = cable.a_terminations.first() %}{% set b = cable.b_terminations.first() %}PP{{a.device.rack.name}}-{{a.name}} / PP{{b.device.rack.name}}-{{b.name}} / {{cable.color|default('BLU')|upper|truncate(3,True,'')}}"
```
Example output: `PPR1A-24 / PPR2B-12 / BLU`

## Network Infrastructure Templates

### Structured Cabling Template
```python
"label_template": "{{cable.a_terminations.first().device.location.name|default(cable.a_terminations.first().device.site.name)}}.{{cable.a_terminations.first().device.name}}.{{cable.a_terminations.first().name}}--{{cable.b_terminations.first().device.location.name|default(cable.b_terminations.first().device.site.name)}}.{{cable.b_terminations.first().device.name}}.{{cable.b_terminations.first().name}}"
```
Example output: `Floor2.IDF2.SW01.gi1--Floor1.MDF.CORE01.te1/1/1`

### Fiber Optic Template
```python
"label_template": "{% if 'fiber' in cable.type|lower or 'sm' in cable.type|lower or 'mm' in cable.type|lower %}FO-{% endif %}{{cable.a_terminations.first().device.rack.name}}-{{cable.a_terminations.first().name}}/{{cable.b_terminations.first().device.rack.name}}-{{cable.b_terminations.first().name}}/{{cable.type|upper}}/{{cable.color|default('YEL')|upper}}"
```
Example output: `FO-R1A-LC1/R2B-LC1/SM-OS2/YEL`

## Available Cable Object Attributes

Common attributes available in templates:

- `cable.pk` - Unique cable ID
- `cable.type` - Cable type (CAT6, CAT6A, SM-OS2, etc.)
- `cable.status` - Cable status
- `cable.color` - Cable color
- `cable.length` - Cable length
- `cable.length_unit` - Length unit
- `cable.description` - Cable description
- `cable.comments` - Cable comments
- `cable.tags` - Cable tags

For terminations (using `cable.a_terminations.first()` or `cable.b_terminations.first()`):
- `.device` - Connected device
- `.device.name` - Device name
- `.device.site` - Device site
- `.device.rack` - Device rack
- `.device.location` - Device location
- `.device.position` - Rack position
- `.device.face` - Rack face (front/rear)
- `.name` - Interface/port name

## Template Functions and Filters

Jinja2 filters that can be used:
- `|upper` - Convert to uppercase
- `|lower` - Convert to lowercase
- `|default('value')` - Provide default value
- `|truncate(n,True,'')` - Truncate to n characters
- `|first` - Get first character
- `|stringformat:'05d'` - Format number with padding

## Testing Templates

Before deploying a template, test it using Django shell:

```python
from dcim.models import Cable
from netbox_cable_labels.utils import render_label

# Get a sample cable
cable = Cable.objects.first()

# Test your template
from jinja2 import Environment, BaseLoader
env = Environment(loader=BaseLoader)
template_string = "Your template here"
template = env.from_string(template_string)
result = template.render(cable=cable)
print(result)
```

## Best Practices

1. **Keep labels concise** - Most label makers have character limits
2. **Use consistent formatting** - Uppercase for static text, consistent separators
3. **Include unique identifiers** - Always include cable.pk or another unique ID
4. **Consider label maker constraints** - Some characters may not print well
5. **Test with edge cases** - Cables without racks, locations, or complete terminations
6. **Use defaults** - Provide fallback values for optional fields