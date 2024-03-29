# -*- coding: utf-8 -*-
# Note to self: the bluetooth widget is basically useless:
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen, ScratchPad, DropDown
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
  Key([mod], "space", lazy.spawn("rofi -show combi"), desc="spawn rofi"),
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

       Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
       Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
       Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
       Key([mod], "k", lazy.layout.up(), desc="Move focus up"),



    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),  desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),  desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),  desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
   

    Key(["mod4"], "space",  lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod, "shift", "control"], "h", lazy.layout.swap_column_left()),
    Key([mod, "shift", "control"], "l", lazy.layout.swap_column_right()),
    Key([mod, "shift"], "space", lazy.layout.flip()),


         Key(["mod4"], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key(["mod4"], "l",
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
             desc='window between minimum and maximum sizes'
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
    keys.append(Key([mod], "e", lazy.group["scratchpad"].dropdown_toggle("term")))
    keys.append(Key([mod], "f", lazy.group["scratchpad"].dropdown_toggle("ranger")))


# Append ScratchPad to groups list: 

groups.append(
        ScratchPad("scratchpad", [
            DropDown("term", "alacritty", width=0.8, height=0.4),
            DropDown('ranger', "alacritty -e'ranger'", width=0.7, height=0.7, x=0.15, y=0.15, opacity=1.0, on_focus_lost_hide=False), #figure sth out here. 
            ]),        
        )





colors = [
    ["#24283b", "#24283b"],  # 0 Tokyo night background
	["#1a1b26", "#1a1b26"],  # 1 background of tokyo night darker
	["#c0caf5", "#c0caf5"],  # 2 white
	["#f7768e", "#f7768e"],  # 3 red
	["#9ece6a", "#9ece6a"],  # 4 green
	["#d08770", "#d08770"],  # 5 orange
	["#7dcfff", "#7dcfff"],  # 6 blue
	["#7aa2f7", "#7aa2f7"],  # 7 blue-purple
	["#bb9af7", "#bb9af7"],  # 8 purple
	["#a9b1d6", "#a9b1d6"],  # 9 Tokyo night editor foreground
]
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

#Layouts:
layout_theme = {"border_width": 3,
                "margin": 2,
                "border_focus": "#7aa2f7",
                "border_normal": "#1E222A",
                }

layouts = [
layout.MonadTall(**layout_theme,ratio=0.55,),
layout.MonadWide(**layout_theme),
layout.Max(**layout_theme),
layout.Columns(**layout_theme),
 layout.Stack(num_stacks=2,**layout_theme),
]

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])

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
widget.Spacer(
    length = 5,
    background = colors[0]
            ),


widget.Image(filename='~/.config/qtile/eos-c.png', margin=3, background="#2f343f", mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("rofi -show combi")}),
widget.GroupBox(
    font = "Source Code Pro",
    disable_drag = True,
    fontsize = 18,
    margin_y = 3,
    margin_x = 15,
    padding_y = 2,
    padding_x = 0,
    borderwidth = 4,
    active = colors[7],
    inactive = colors[2],
    rounded = True,
    highlight_color = colors[1],
    highlight_method = "line",
    this_current_screen_border = colors[7],
    this_screen_border = colors [8],
    other_current_screen_border = colors[8],
    other_screen_border = colors[3],
    foreground = colors[2],
    background = colors[0]
),
# Centre of the bar----------------------------------------
widget.Spacer(
    length = 8,
    background = colors[0]
),
widget.NetGraph(
    background = colors[0]
),
widget.Systray(
    background = colors[0]
),
widget.TaskList(
   border = colors[7],
   font = "Source Code Pro Medium",
   hightlight_method = "block", 
    ),
#widget.Spacer(
#    length = bar.STRETCH,
#    background = colors[1]
#),
###Right-side of bar---------------------------------
widget.TextBox(
    text = "  ",
    padding = 2,
    foreground = colors[3],
    background = colors[0],
    fontsize = 17,
    font = "Iosevka Nerd Font",
),
widget.CurrentLayout(
    font = "Source Code Pro Medium",
    fontsize = 16,
    foreground = colors[3],
    background = colors[0]
),
widget.TextBox(
    font="FontAwesome",
    text=" ",
    foreground=colors[5],
    background=colors[0],
    padding = 0,
    fontsize=18
),
widget.Battery(
    font="Noto Sans",
    format = "{percent:2.0%}",
    update_interval = 60,
    fontsize = 16,
    foreground = colors[5],
    background = colors[0],
),
    widget.TextBox(
        text="",
        foreground = colors[4],
        background = colors[0],
    ),
    widget.Backlight(
        foreground = colors[4],
        background = colors[0],
        backlight_name="intel_backlight",
    ),
widget.TextBox(
    text = " ",
    foreground = colors[6],
    background = colors[0],
    padding = 0,
    fontsize=16,
    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("pavucontrol")}
),
widget.Volume(
    foreground = colors[6],
    background = colors[0],
    padding = 5,
    fontsize = 16,
    update_interval = 0.1,
    step = 5
),
widget.Clock(
    font = "Source Code Pro Medium",
    format = '  %d-%m %Y %a %I:%M %p',
    fontsize = 16,
    foreground = colors[8],
    background = colors[0]
),
  widget.TextBox(
    text='',
    mouse_callbacks= {'Button1':lambda: qtile.cmd_spawn(os.path.expanduser('~/.config/rofi/powermenu.sh'))},
    foreground = colors[9],
),
]
    return widgets_list


# screens/bar (need to make changes to the code in the future)

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
