#!/bin/bash

set -uxe

# If host mounted a manually-created MediaGoblin config file, make a copy that
# the MediaGoblin user can access it.
if [ -e ./static/mediagoblin_host.ini ]; then
  >&2 echo "Using host-defined ./static/mediagoblin.ini file"
  cp ./static/mediagoblin_host.ini mediagoblin.ini
  chown "$MEDIAGOBLIN_USER:$MEDIAGOBLIN_GROUP" mediagoblin.ini
else
  >&2 echo "No host-defined mediagoblin.ini file, using default"
fi

if [ -e ./static/init-mediagoblin.sh ]; then
  >&2 echo "Using host-defined ./static/init-mediagoblin.sh file"
  cp ./static/init-mediagoblin.sh init-mediagoblin.sh
  chown "$MEDIAGOBLIN_USER:$MEDIAGOBLIN_GROUP" mediagoblin.ini
else
  >&2 echo "No host-defined init-mediagoblin.sh file, using default"
fi

chown \
  --no-dereference \
  --recursive \
  "${MEDIAGOBLIN_USER}:${MEDIAGOBLIN_GROUP}" "$MEDIAGOBLIN_HOME_DIR"

su "$MEDIAGOBLIN_USER" -c './user-dev-workaround.sh'
su "$MEDIAGOBLIN_USER" -c './init-mediagoblin.sh'
su "$MEDIAGOBLIN_USER" -c './lazyserver.sh --server-name=broadcast'
