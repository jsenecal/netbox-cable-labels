#!/bin/bash

USER=ubuntu

sudo chown -R ${USER}:${USER} /etc/netbox/scripts

# Reconfigure User id if set by user
if [ ! -z "${USER_UID}" ] && [ "${USER_UID}" != "`id -u ${USER}`" ] ; then
  echo -n "Update uid for user ${USER} with ${USER_UID}"
  usermod -u ${USER_UID} ${USER}
  echo "... updated"
else
  echo "skipping UID configuration"
fi

if [ -n "${USER_GID}" ] && [ "${USER_GID}" != "`id -g ${USER}`" ] ; then
  echo -n "Update gid for group ${USER} with ${USER_GID}"
  usermod -u ${USER_UID} ${USER}
  echo "... updated"
else
  echo "skipping GID configuration"
fi

# Install pre-commit hooks if in a git repo
if [ -d "/opt/netbox-cable-labels/.git" ]; then
  cd /opt/netbox-cable-labels
  pre-commit install --install-hooks 2>/dev/null || true
fi

# Load demo data first, then run appropriate migrations
DEMO_DATA_MARKER="/opt/netbox/.demo-data-loaded"
DEMO_DATA_LOADED=false

if [ ! -f "$DEMO_DATA_MARKER" ] && [ "${LOAD_DEMO_DATA:-true}" = "true" ]; then
  echo "Loading NetBox demo data..."
  NETBOX_VERSION=$(cd /opt/netbox/netbox && /opt/netbox/venv/bin/python -c "from netbox.settings import RELEASE; print('.'.join(RELEASE.version.split('.')[:2]))" 2>/dev/null | tail -1)
  DEMO_SQL_URL="https://raw.githubusercontent.com/netbox-community/netbox-demo-data/master/sql/netbox-demo-v${NETBOX_VERSION}.sql"

  if curl -sfL "$DEMO_SQL_URL" -o /tmp/netbox-demo.sql; then
    export PGPASSWORD="${DB_PASSWORD:-netbox}"
    if psql -h "${DB_HOST:-postgres}" -U "${DB_USER:-netbox}" -d "${DB_NAME:-netbox}" < /tmp/netbox-demo.sql 2>/dev/null; then
      touch "$DEMO_DATA_MARKER"
      DEMO_DATA_LOADED=true
      echo "Demo data loaded successfully."
    else
      echo "Warning: Failed to load demo data (database may not be ready yet)."
    fi
    rm -f /tmp/netbox-demo.sql
  else
    echo "Warning: Demo data not available for NetBox v${NETBOX_VERSION}."
  fi
fi

# Run migrations based on whether demo data was loaded
if [ "$DEMO_DATA_LOADED" = true ] || [ -f "$DEMO_DATA_MARKER" ]; then
  echo "Running plugin migrations only..."
  /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py migrate netbox_cable_labels --no-input 2>/dev/null || echo "No plugin migrations to apply."
else
  echo "Running all database migrations..."
  /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py migrate --no-input
fi

exec "$@"
