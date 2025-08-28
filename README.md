# NetBox Auto Cable Label Plugin

Plugin for netbox that allows the automatic generation of the label field content for cables based on a user defined template

* Free software: Apache-2.0

## Compatibility

| NetBox Version | Plugin Version |
|----------------|----------------|
|     4.x        |      0.1.x     |


## Installing

For adding to a NetBox Docker setup see
[the general instructions for using netbox-docker with plugins](https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins).

### Install from PyPI

```bash
pip install netbox-cable-labels
```

### Install from GitHub

```bash
pip install git+https://github.com/jsenecal/netbox-cable-labels
```

or by adding to your `local_requirements.txt` or `plugin_requirements.txt` (netbox-docker):

```bash
netbox-cable-labels
```

Enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`,
 or if you use netbox-docker, your `/configuration/plugins.py` file :

```python
PLUGINS = [
    'netbox_cable_labels'
]
```


## Configuring

Setup PLUGINS_CONFIG with the following:
```python
PLUGINS_CONFIG = {
    "netbox_cable_labels": {"label_template": "Some Jinja2 template string here"},
}
```

> Please note that the cable instance is passed as `cable` to the templating engine.

### Default configuration

By default, the plugin copies the cable `id` in the label, prefixed with the pound (#) sign.

```
"#{{cable.pk}}"
```

## Management command

Using `manage.py`, you can run the command `generate_labels` to automatically generate labels on cables that do not already have one set, based on the configured template.

```
./manage.py generate_labels
```
