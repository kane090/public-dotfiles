#!/bin/sh
nm-applet --indicator &
xsetroot -cursor_name left_ptr &
$HOME/.fehbg &
#setxkbmap -layout us,ru -option grp:alt_space_toggle &
dex -a -s /etc/xdg/autostart/:~/.config/autostart &
