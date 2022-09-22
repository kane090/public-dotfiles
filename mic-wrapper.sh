#!/bin/bash

# Get UID of user running pulseaudio (uses the first if more than one)
PUID=`ps -C pipewire -o ruid= | awk '{print $1}'`

if [ ! -z "$PUID" ]; then
  # environment variables to export
  export PULSE_RUNTIME_PATH="/var/run/user/$PUID/pulse"
  export HOME=`getent passwd $PUID | cut -d: -f6`

  if [ -x "$HOME/.set-microphone.sh" ]; then
    nohup sudo -u "#$PUID" -E $HOME/.set-microphone.sh >/dev/null 2>&1 &
  fi

fi
