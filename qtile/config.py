# -*- coding: utf-8 -*-
# Note to self: the bluetooth widget is basically useless:
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401

mod = "mod1"                                     # Sets mod key to alt, mod4 is windows key
myTerm = "alacritty"                             # My terminal of choice

#Keybindings:

keys = [ ### Basics
         Key([mod], "Return",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([mod], "space",
             lazy.spawn("dmenu_run -fn 'Source Code Pro -30'"),
            desc='Run Launcher'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
     Key([mod, "shift"], "Tab",
             lazy.prev_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "shift"], "q",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod], "p",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "i",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         Key([mod, "shift"], "Return",
             lazy.spawn("emacsclient -c -a emacs"),
             desc='Doom Emacs'
             ),
          Key([mod, "shift"], "e", lazy.spawn('firefox'), desc="Launches Firefox Web Browser"),
          Key([mod, "shift"], "f", lazy.spawn('pcmanfm'), desc="Launches File Manager"),

         ### Window controls

       Key([mod], "j",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "k",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),

         Key([mod], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "g",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
          Key([mod], "g",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         #### Stack controls
          Key([mod], "d",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "shift"], "d",
             lazy.layout.up(),
             desc='reverse of teh above command'
             ),
         ### Switch focus to specific monitor (out of three)
         Key([mod], "w",
             lazy.to_screen(0),
             desc='Keyboard focus to monitor 1'
             ),
         Key([mod], "e",
             lazy.to_screen(1),
             desc='Keyboard focus to monitor 2'
             ),
         Key([mod], "r",
             lazy.to_screen(2),
             desc='Keyboard focus to monitor 3'
             ),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),

    #Brightness, Alsa, Screenshots-------------------------------------------------------------------------

#####Brightness
Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set 5%+")),
Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
#####Screenshots
Key([], "Print", lazy.spawn("scrot -s ./screenshot/%Y-%m-%d-%T-screenshot.png")),
Key([mod], "Print", lazy.spawn("scrot ./screenshot/%Y-%m-%d-%T-screenshot.png")),
#####Media Keys
Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 5%+")),
Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 5%-")),
Key([], "XF86AudioMute", lazy.spawn("amixer -D pulse set Master 1+ toggle")),
]

#Workspaces:
group_names = [("", {'layout': 'monadwide'}),
               ("", {'layout': 'monadtall'}),#
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'ratiotile'}),
               ("", {'layout': 'ratiotile'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

colors = [
 	["#1E222A", "#1E222A"],  # 0 super dark one-dark background,very similar to the super dark nordic background
	["#3b4252", "#3b4252"],  # 1 background lighter
	["#81a1c1", "#81a1c1"],  # 2 foreground
	["#bf616a", "#bf616a"],  # 3 red
	["#a3be8c", "#a3be8c"],  # 4 green
	["#ebcb8b", "#ebcb8b"],  # 5 yellow
	["#81a1c1", "#81a1c1"],  # 6 blue
	["#d8dee9", "#d8dee9"],  # 7 white
	["#88c0d0", "#88c0d0"],  # 8 cyan
	["#b48ead", "#b48ead"],  # 9 magenta
	["#4c566a", "#4c566a"],  # 10 grey
	["#d08770", "#d08770"],  # 11 orange
	["#8fbcbb", "#8fbcbb"],  # 12 super cyan
	["#5e81ac", "#5e81ac"],  # 13 super blue
        ["#333945", "#333945"],  # 14 one dark black-bright(doom emac's highlighted text color)
]
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

#Layouts:
layout_theme = {"border_width": 3,
                "margin": 2,
                "border_focus": "#5e81ac",
                "border_normal": "#1E222A",
                }

layouts = [
layout.MonadTall(**layout_theme,ratio=0.55,),
layout.MonadWide(**layout_theme),
layout.Max(**layout_theme),
]

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Source Code Pro Medium",
    fontsize = 16,
    padding = 8,
    foreground = colors[2],
    background=colors[1]
)
extension_defaults = widget_defaults.copy()


#### Mouse_callback functions

def open_powermenu():
	qtile.cmd_spawn("systemctl suspend")

#### Widgets and Bar

def init_widgets_list():
    widgets_list = [
            widget.Spacer(
                length = 2,
                background = colors[0]
            ),

# Left Side of the bar-------------------------------------
widget.GroupBox(
    font = "Source Code Pro",
    disable_drag = True,
    fontsize = 18,
    margin_y = 3,
    margin_x = 15,
    padding_y = 2,
    padding_x = 0,
    borderwidth = 4,
    active = colors[2],
    inactive = colors[7],
    rounded = True,
    highlight_color = colors[1],
    highlight_method = "line",
    this_current_screen_border = colors[2],
    this_screen_border = colors [4],
    other_current_screen_border = colors[8],
    other_screen_border = colors[3],
    foreground = colors[2],
    background = colors[0]
),
# Centre of the bar----------------------------------------
widget.Spacer(
    length = 8,
    background = colors[14]
),
widget.TextBox(
    font = "Iosevka Nerd Font",
    fontsize = 18,
    text = "",
    foreground = colors[13],
    background = colors[14]
),
widget.CPU(
    font = "Source Code Pro Medium",
    format = "{load_percent}%",
    fontsize = 16,
    foreground = colors[13],
    background = colors[14],
    update_interval = 5
),
widget.TextBox(
    font = "Iosevka Nerd Font",
    fontsize = 18,
    text = "",
    foreground = colors[5],
    background = colors[14]
),
widget.Memory(
    font = "Source Code Pro Medium",
    fontsize = 16,
    format = "{MemUsed:.0f}{mm}",
    foreground = colors[5],
    background = colors[14],
    update_interval = 5
),
widget.TextBox(
    font = "Iosevka Nerd Font",
    fontsize = 17,
    text = "",
    foreground = colors[12],
    background = colors[14]
),
widget.NvidiaSensors(
    font = "Source Code Pro Medium",
    fontsize = 16,
    foreground = colors[12],
    foreground_alert = colors[2],
    background = colors[14],
    update_interval = 5
),
widget.NetGraph(
    background = colors[14]
),
widget.Systray(
    background = colors[14]
),
widget.Spacer(
    length = bar.STRETCH,
    background = colors[14]
),
###Right-side of bar---------------------------------
widget.TextBox(
    text = "  ",
    padding = 2,
    foreground = colors[7],
    background = colors[0],
    fontsize = 17,
    font = "Iosevka Nerd Font",
),
widget.CurrentLayout(
    font = "Source Code Pro Medium",
    fontsize = 16,
    foreground = colors[7],
    background = colors[0]
),
widget.TextBox(
    font="FontAwesome",
    text=" ",
    foreground=colors[9],
    background=colors[0],
    padding = 0,
    fontsize=18
),
widget.Battery(
    font="Noto Sans",
    format = "{percent:2.0%}",
    update_interval = 60,
    fontsize = 16,
    foreground = colors[9],
    background = colors[0],
),
widget.TextBox(
    text = " Vol",
    foreground = colors[8],
    background = colors[0],
    padding = 0,
    fontsize=16
),
widget.Volume(
    foreground = colors[8],
    background = colors[0],
    padding = 5,
    fontsize = 16,
    update_interval = 0.1,
    step = 5
),
widget.TextBox(
    font = "Iosevka Nerd Font",
    fontsize = 18,
    text = "",
    foreground = colors[4],
    background = colors[0]
),
widget.Clock(
    font = "Source Code Pro Medium",
    format = '%a %d %b(%m)',
    fontsize = 16,
    foreground = colors[4],
    background = colors[0]
),
widget.Clock(
    font = "Source Code Pro Medium",
    format = '%I:%M:%S %p ',
    fontsize = 16,
    foreground = colors[4],
    background = colors[0]
),
widget.TextBox(
    text="⏻",
    foreground=colors[3],
    background=colors[0],
    font="Font Awesome 5 Free Solid",
    fontsize=23,
    padding= 2,
    mouse_callbacks={"Button1": open_powermenu},
),
widget.Spacer(
    length = 5,
    background = colors[0]
            )
]
    return widgets_list


# screens/bar

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[7:8]               # Slicing removes unwanted widgets (systray) on Monitors 1,
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():#margin = (above bar, left of bar, below bar, right of bar)
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=30,  opacity=1.0,bottom=bar.Gap(18),left=bar.Gap(18),right=bar.Gap(18), margin=[0,0,0,0])),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=0.9,bottom=bar.Gap(18),left=bar.Gap(18),right=bar.Gap(18), size=35, margin=[0,0,0,0])),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.9,bottom=bar.Gap(18),left=bar.Gap(18),right=bar.Gap(18), size=35, margin=[0,0,0,0]))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

# assign apps to groups/workspace
@hook.subscribe.client_new
def assign_app_group(client):
    d = {}
# assign deez apps
    d[group_names[0][0]] = ['firefox']
    d[group_names[1][0]] = []
    d[group_names[2][0]] = []
    d[group_names[3][0]] = []
    d[group_names[4][0]] = []
    d[group_names[5][0]] = []
    d[group_names[6][0]] = []
    d[group_names[7][0]] = []
    d[group_names[8][0]] = []

    wm_class = client.window.get_wm_class()[0]
    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen(toggle=False)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
