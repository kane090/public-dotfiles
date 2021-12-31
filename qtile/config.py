# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
import psutil

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"
alt = "mod1"
terminal = "alacritty"

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "shift"], "h", lazy.layout.swap_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.swap_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "o", lazy.layout.grow(), desc="Grow window"),
    Key([mod, "shift"], "i", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod, "shift"], "n", lazy.layout.reset(), desc="Reset layout"),
    Key([mod, "shift"], "space", lazy.layout.flip(), desc="Flip left and right sides"),

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Put the focused window to/from floating mode"),
    Key([mod], "m", lazy.window.toggle_fullscreen(), desc="Put the focused window to/from fullscreen mode"),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, alt], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, alt], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    Key([mod], "n", lazy.spawn("thunar"), desc="Launch file manager"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launch run prompt"),
    Key([mod], "w", lazy.spawn("firefox"), desc="Launch web browser"),
    Key([mod], "e", lazy.spawn("mailspring"), desc="Launch email client"),
    Key([mod], "bracketleft", lazy.spawn("discord"), desc="Launch Discord"),
    Key([mod], "bracketright", lazy.spawn("spotify -no-zygote"), desc="Launch Spotify"),
    
    Key([mod], "x", lazy.spawn("betterlockscreen -l dimblur --off 1"), desc="Lock desktop"),
    Key([mod, "shift"], "p", lazy.spawn(".config/rofi/powermenu.sh"), desc="Launch power menu"),
    
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+ unmute"), desc="Raise volume by 5%"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%- unmute"), desc="Lower volume by 5%"),
    Key([], "XF86AudioMute", lazy.spawn("aamixer -D pulse sset Master toggle-mute"), desc="Toggle mute"),
]

groups = [Group(i) for i in "1234"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
        #     desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.MonadTall(border_focus='#8a8a8a', margin=8, single_margin=8, single_border_width=3, border_width=3),
    layout.Matrix(border_focus='#8a8a8a', margin=2, border_width=3),
    # Try more layouts by unleashing below layouts.
    # layout.Columns(border_focus_stack=['#d75f5f', '#8f3d3d'], border_width=4),
    # layout.Max(),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

colors = [
    ['#00000000','#00000000'],
    ['#3b3b3b', '#3b3b3b'],
    ['#fff', '#fff'],
    ['#ff0000', '#ff0000'],
    ['#ff7c2b', '#ff7c2b'],
    ['#edff29', '#edff29'],
    ['#00b339', '#00b339'],
    ['#00e5ff', '#00e5ff'],
    ['#dd45ff', '#dd45ff'],
]

widget_defaults = dict(
    font='NotoSans Nerd Font',
    fontsize=15,
    padding=6,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(highlight_method='block', this_current_screen_border=colors[1], urgent_alert_method='block', block_highlight_text_color=colors[7]),
                widget.Sep(linewidth=0, padding=15),
                widget.WindowName(foreground=colors[4]),
                widget.Mpris2(objname='org.mpris.MediaPlayer2.spotify', name='spotify', display_metadata=['xesam:artist', 'xesam:title'], scroll_chars=0, foreground=colors[6]),
                widget.TextBox(update_interval=1, func=lambda: subprocess.check_output("python /home/rn/.config/polybar/spotify_script.py").decode('UTF-8')),
                widget.OpenWeather(location='Moscow,RU', format='Weather: {main_temp} °{units_temperature} {weather_details}', foreground=colors[7]),
                widget.CurrentLayout(foreground=colors[5]),
                widget.CPU(format='CPU: {load_percent}%', foreground=colors[6]),
                widget.Memory(format='Memory: {MemPercent}%', foreground=colors[4]),
                widget.Volume(foreground=colors[7]),
                widget.CheckUpdates(no_update_string='No updates', colour_no_updates=colors[5], foreground=colors[5], custom_command="./updates-pacman-aurhelper.sh"),
                #widget.ThermalSensor(),
                widget.KeyboardLayout(configured_keyboards=['us','ru'], foreground=colors[3]),
                widget.Clock(format='%a %d %b %Y %H:%M:%S', foreground=colors[8]),
                widget.Systray(),
            ],
            26, background=colors[0],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([alt], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([alt], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([alt], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
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
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostartonce.sh')
    subprocess.call([home])

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
