#!/bin/sh

focused_desktop=$(bspc query -D -d focused --names)
current_layout=$(bsp-layout get $focused_desktop)

echo "$current_layout"
