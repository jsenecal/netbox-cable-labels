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

exec "$@"
