# -*- coding: utf-8 -*-
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

mod = "mod1"                                     # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"                             # My terminal of choice

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([mod], "d",
            #lazy.spawn("wofi --show drun -config ~/.config/wofi/config -style ~/.config/wofi/style.css"),
             lazy.spawn("rofi -show drun -config ~/.config/rofi/launchers/text/style_4.rasi"),
            desc='Run Launcher'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
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
         Key([mod, "shift"], "p",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),

         #Key([mod, "shift"], "Return",
             #lazy.spawn("emacsclient -c -a emacs"),
             #desc='Doom Emacs'
             #),
          Key([mod, "shift"], "e", lazy.spawn('firefox'), desc="Launches Firefox Web Browser"),
          Key([mod, "shift"], "f", lazy.spawn('pcmanfm'), desc="Launches Pcmanfm File Manager"),
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
         ### Treetab controls
          Key([mod, "shift"], "h",
             lazy.layout.move_left(),
             desc='Move up a section in treetab'
             ),
         Key([mod, "shift"], "l",
             lazy.layout.move_right(),
             desc='Move down a section in treetab'
             ),
         ### Window controls
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
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
         Key(["control", "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
          Key([mod], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "shift"], "space",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),
        ### Brightness, Alsa, Screenshots...

    #Brightness

  Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set 10%+")),
  Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

	#Atalhos
	  Key([], "Print", lazy.spawn("flameshot gui")),

	#Media Keys
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 5%-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer -D pulse set Master 1+ toggle")),

         # Emacs programs launched using the key chord CTRL+e followed by 'key'
         KeyChord(["control"],"e", [
             Key([], "e",
                 lazy.spawn("emacsclient -c -a 'emacs'"),
                 desc='Launch Emacs'
                 ),
             Key([], "b",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(ibuffer)'"),
                 desc='Launch ibuffer inside Emacs'
                 ),
             Key([], "d",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(dired nil)'"),
                 desc='Launch dired inside Emacs'
                 ),
             Key([], "i",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(erc)'"),
                 desc='Launch erc inside Emacs'
                 ),
             Key([], "m",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(mu4e)'"),
                 desc='Launch mu4e inside Emacs'
                 ),
             Key([], "n",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(elfeed)'"),
                 desc='Launch elfeed inside Emacs'
                 ),
             Key([], "s",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(eshell)'"),
                 desc='Launch the eshell inside Emacs'
                 ),
             Key([], "v",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(+vterm/here nil)'"),
                 desc='Launch vterm inside Emacs'
                 )
         ]),
]

#Workspaces:
group_names = [("I", {'layout': 'monadtall'}),
               ("II", {'layout': 'monadtall'}),
               ("III", {'layout': 'ratiotile'}),
               ("IV", {'layout': 'stack'}),
               ("V", {'layout': 'monadtall'}),
               ("VI", {'layout': 'max'}),
               ("VII", {'layout': 'treetab'}),
               ("VIII", {'layout': 'floating'}),
               ("IX", {'layout': 'ratioTile'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group


colors = [["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#ecbbfb", "#ecbbfb"]] # backbround for inactive screens

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

#Layouts:


layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme,
                      ratio=0.6,
                     ),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
         font = "Ubuntu",
         fontsize = 10,
         sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
         section_fontsize = 10,
         border_width = 2,
         bg_color = "1c1f24",
         active_bg = "c678dd",
         active_fg = "000000",
         inactive_bg = "a9a1e1",
         inactive_fg = "1c1f24",
         padding_left = 0,
         padding_x = 0,
         padding_y = 5,
         section_top = 10,
         section_bottom = 20,
         level_shift = 8,
         vspace = 3,
         panel_width = 200
         ),
    layout.Floating(**layout_theme)
]

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Source Code Pro Medium",
    fontsize = 20,
    padding = 5,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
            widget.Spacer(
                length = 2,
                background = colors[1]
            ),

            # Left Side of the bar

             widget.Sep(
                linewidth = 3,
                background = colors[1]
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 20,
                text = "﬙",
                foreground = colors[6],
                background = colors[1]
            ),
            widget.CPU(
                font = "Source Code Pro Medium",
                format = "{load_percent}%",
                fontsize = 20,
                foreground = colors[2],
                background = colors[1],
                update_interval = 5
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 20,
                text = "",
                foreground = colors[5],
                background = colors[1]
            ),
            widget.Memory(
                font = "Source Code Pro Medium",
                format = "{MemUsed:.0f}{mm}",
                foreground = colors[2],
                background = colors[1],
                update_interval = 5
            ),
           widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 20,
                text = "",
                foreground = colors[5],
                background = colors[1]
            ),
            widget.Net(
                format = "{down} ↓↑ {up}",
                foreground = colors[2],
                background = colors[1],
                update_interval = 5
            ),
           widget.Spacer(
                length = bar.STRETCH,
                background = colors[1]
            ),

            # Center bar
            widget.TextBox(
                       text = "",
                       padding = 2,
                       foreground = colors[2],
                       background = colors[4],
                       fontsize = 24
                       ),
            widget.CheckUpdates(
                       update_interval = 1800,
                       distro = "Arch_checkupdates",
                       display_format = "{updates} Updates",
                       foreground = colors[2],
                       mouse_callbacks = {'Button1': lazy.spawn(myTerm + 'echo sudo pacman -Syu')},
                       background = colors[4]
                       ),
            widget.Sep(
                linewidth = 3,
                background = colors[1]
            ),
             widget.GroupBox(
                       font = "Source Code Pro",
                       fontsize = 20,
                       margin_y = 3,
                       margin_x = 5,
                       padding_y = 5,
                       padding_x = 5,
                       borderwidth = 5,
                       active = colors[2],
                       inactive = colors[7],
                       rounded = True,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[6],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.Sep(
                linewidth = 3,
                background = colors[1]
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 20,
                text = " ",
                foreground = colors[5],
                background = colors[1]
            ),
            widget.CurrentLayout(
                font = "Source Code Pro Medium",
                fontsize = 20,
                foreground = colors[2],
                background = colors[1]
            ),

            # Left Side of the bar

            widget.Spacer(
                length = bar.STRETCH,
                background = colors[1]
            ),
            widget.Systray(
                        background=colors[1],
                        icon_size=20,
                        padding = 4
                        ),
            widget.Battery(
                      font="Noto Sans",
                         update_interval = 60,
                         fontsize = 20,
                         foreground = colors[5],
                        background = colors[1],
	                     ),
                widget.TextBox(
                         font="FontAwesome",
                         text="  ",
                       foreground=colors[6],
                        background=colors[1],
                         padding = 0,
                         fontsize=20
                         ),
            widget.Sep(
                linewidth = 3,
                background = colors[1]
            ),
            widget.TextBox(
                      text = "",
                       foreground = colors[2],
                       background = colors[5],
                       padding = 0
                       ),
              widget.Volume(
                       foreground = colors[2],
                       background = colors[5],
                       padding = 5
                       ),
            widget.Sep(
                size_percent = 60,
                linewidth = 3,
                background = colors[1]
            ),
            #widget.TextBox(
                #text = "",
                #foreground = colors[2],
                       #background = colors[5],
                       #padding = 0
                       #),
            #widget.Backlight(
                #brightness_file = "intel_backlight",
                #foreground = colors[2],
                       #background = colors[5],
                       #padding = 5
                       #),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 20,
                text = "",
                foreground = colors[7],
                background = colors[1]
            ),
            widget.Clock(
                font = "Source Code Pro Medium",
                format = '%b %d-%Y',
                fontsize = 20,
                foreground = colors[2],
                background = colors[1]
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 20,
                text = "",
                foreground = colors[7],
                background = colors[1]
            ),
            widget.Clock(
                font = "Source Code Pro Medium",
                format = '%I:%M:%S %p',
                fontsize = 20,
                foreground = colors[2],
                background = colors[1]
            ),
            widget.Spacer(
                length = 5,
                background = colors[1]
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

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=45,  opacity=0.9, margin=[5,10,0,10])),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=0.9, size=30, margin=[5,10,0,10])),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.9, size=30, margin=[5,10,0,10]))]

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
#
@hook.subscribe.client_new
def assign_app_group(client):
    d = {}

    # assign deez apps
    d[group_names[0][0]] = ['firefox']
    d[group_names[1][0]] = []
    d[group_names[2][0]] = []
    d[group_names[3][0]] = []
    d[group_names[4][0]] = ['emacs']
    d[group_names[5][0]] = ['pcmanfm']
    d[group_names[6][0]] = ['discord']
    d[group_names[7][0]] = ['vlc', 'obs', 'mpv', 'mplayer', 'lxmusic', 'gimp']
    d[group_names[8][0]] = ['gparted', 'wdisplays', 'pavucontrol']

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
follow_mouse_focus = True
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
