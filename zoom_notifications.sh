#!/bin/sh

if (ps aux | grep '/usr/bin/zoom' | grep -v grep > /dev/null)
then
    killall -SIGUSR1 dunst
else
    killall -SIGUSR2 dunst
fi
