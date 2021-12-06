#!/usr/bin/env bash

nitrogen --restore &
xrandr -s  1920x1200 &
/usr/bin/emacs --daemon &
nm-applet &
xset m 0 0 &
