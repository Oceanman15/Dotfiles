#!/usr/bin/env bash

nitrogen --restore &
/usr/bin/emacs --daemon &
udiskie -t &
nm-applet &
xrandr --output eDP-1 --primary --mode 1920x1080 --pos 0x1080 --output HDMI-1 --mode 1920x1080 --pos 0x0 &
picom &
firefox &


