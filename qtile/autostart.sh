#!/usr/bin/env bash

nitrogen --restore &
# xrandr -s  1920x1200 &
/usr/bin/emacs --daemon &
nm-applet &
xset m 0 0 &
xrandr --output eDP-1 --scale 0.5x0.5 &
#trackpad:
#sources: https://wiki.archlinux.org/title/Touchpad_Synaptics#Using_syndaemon
#https://man.archlinux.org/man/syndaemon.1
#https://man.archlinux.org/man/synaptics.4
syndaemon -i 1.0 -t -K -R -d
synclient TapButton2=3
synclient TapButton1=1
