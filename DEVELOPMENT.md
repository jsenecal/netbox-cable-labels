# Development Guide

This guide will help you set up a development environment for the NetBox Cable Labels plugin.

## Quick Start with VS Code Dev Containers

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Getting Started

1. **Open in Dev Container**
   - Open VS Code
   - Open the command palette (F1 or Cmd/Ctrl+Shift+P)
   - Run "Dev Containers: Open Folder in Container..."
   - Select the `netbox-cable-labels` folder
   - VS Code will build and start the development environment

2. **Access NetBox**
   - URL: http://localhost:8003
   - Username: `admin`
   - Password: `admin`
   - API Token: `0123456789abcdef0123456789abcdef01234567`

3. **Development Workflow**
   - The plugin is installed in development mode (`pip install -e`)
   - Changes to Python files will be reflected immediately after server restart
   - Use VS Code's integrated terminal to run commands

## Development Environment Details

### Services

The dev container includes:

- **NetBox**: Latest version with LDAP support
- **PostgreSQL 15**: Database server
- **Redis 7**: Caching and task queue

### Pre-installed Tools

- **uv**: Fast Python package installer and resolver
- **ruff**: Fast Python linter and formatter (replaces flake8, black, isort)
- Python development tools (ipython, django-debug-toolbar, django-extensions)
- Testing tools (pytest, pytest-django, pytest-cov, factory-boy)
- Git and git-flow

### Sample Data

The environment includes sample data for testing:
- Site: "Sample Site"
- Rack: "Rack 1A"
- Devices: switch-01, switch-02
- Sample cable with auto-generated label

## Common Development Tasks

### Running Tests

```bash
# Run all tests
pytest /opt/netbox-cable-labels/netbox_cable_labels/tests/

# Run specific test file
pytest /opt/netbox-cable-labels/netbox_cable_labels/tests/test_utils.py

# Run with coverage
pytest --cov=netbox_cable_labels /opt/netbox-cable-labels/netbox_cable_labels/tests/
```

### Django Management Commands

```bash
# Django shell
/opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py shell

# Generate labels for existing cables
/opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py generate_labels

# Create migrations (if adding models)
/opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py makemigrations netbox_cable_labels

# Apply migrations
/opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py migrate
```

### Code Quality

```bash
# Format code with ruff
ruff format /opt/netbox-cable-labels/netbox_cable_labels/

# Lint and auto-fix code with ruff
ruff check --fix /opt/netbox-cable-labels/netbox_cable_labels/

# Check without fixing
ruff check /opt/netbox-cable-labels/netbox_cable_labels/
```

### Package Management with uv

```bash
# Install a package
uv pip install --system <package-name>

# Install development dependencies
uv pip install --system -r requirements-dev.txt

# Install the plugin in editable mode
uv pip install --system -e /opt/netbox-cable-labels

# Show installed packages
uv pip list

# Upgrade a package
uv pip install --system --upgrade <package-name>
```

### Debugging

1. **Django Debug Toolbar**: Available in the browser when DEBUG=True
2. **IPython Shell**: Use for interactive debugging
   ```python
   from dcim.models import Cable
   from netbox_cable_labels.utils import render_label
   
   cable = Cable.objects.first()
   label = render_label(cable)
   print(label)
   ```

3. **VS Code Debugging**: Launch configurations are pre-configured

## Working with the Plugin

### Testing Label Templates

```python
# In Django shell
from dcim.models import Cable
from netbox_cable_labels.utils import render_label
from django.conf import settings

# Test with a specific cable
cable = Cable.objects.first()
print(f"Cable ID: {cable.pk}")
print(f"Generated Label: {render_label(cable)}")

# Test with custom template
from jinja2 import Environment, BaseLoader
env = Environment(loader=BaseLoader)
template = env.from_string("Custom-{{cable.pk}}")
print(template.render(cable=cable))
```

### Creating Test Cables

```python
from dcim.models import Cable, Interface

# Get two interfaces
int1 = Interface.objects.filter(device__name='switch-01').first()
int2 = Interface.objects.filter(device__name='switch-02').first()

# Create a cable
cable = Cable(
    type='cat6a',
    status='connected',
    color='red',
    length=10,
    length_unit='m'
)
cable.save()
cable.a_terminations.set([int1])
cable.b_terminations.set([int2])
cable.save()

print(f"Created cable {cable.pk} with label: {cable.label}")
```

## Troubleshooting

### Container won't start
- Check Docker is running
- Ensure ports 8000, 5432, 6379 are not in use
- Try rebuilding: "Dev Containers: Rebuild Container"

### Plugin not loading
- Check `PLUGINS` setting in configuration.py
- Verify plugin is installed: `pip show netbox-cable-labels`
- Check NetBox logs for errors

### Database errors
- Ensure migrations are applied
- Try resetting database: 
  ```bash
  docker-compose down -v
  docker-compose up -d
  ```

## Additional Resources

- [NetBox Documentation](https://docs.netbox.dev/)
- [NetBox Plugin Development](https://docs.netbox.dev/en/stable/plugins/development/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)