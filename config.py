# Imports
from os import environ
from socket import gethostname
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from random import choice
from subprocess import run

mod = "mod4"
terminal = "xfce4-terminal"

outer_gap = 15
inner_gap = 10

accent_colors = [
    "#b48ead",
    "#a3be8c",
    "#ebcb8b",
    "#bf616a",
    "#81a1c1",
    "#88c0d0",
]

accent_color = accent_colors[4]
# accent_color = choice(accent_colors)
run(f'xsetroot -solid "{accent_color}"', shell=True)

# Keybindings
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    Key(
        [mod, "shift"],
        "Tab",
        lazy.layout.previous(),
        desc="Move window focus to other window",
    ),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [
    Group(**i)
    for i in [
        {"name": "DEV", "layout": "spiral"},
        {"name": "WWW", "layout": "spiral"},
        {"name": "SYS", "layout": "spiral"},
        {"name": "DOC", "layout": "spiral"},
        {"name": "VBOX", "layout": "spiral"},
        {"name": "CHAT", "layout": "spiral"},
        {"name": "MUS", "layout": "spiral"},
        {"name": "VID", "layout": "spiral"},
        {"name": "GFX", "layout": "spiral"},
    ]
]

for i, group in enumerate(groups):
    keys.extend(
        [
            # mod1 + number of group = switch to group
            Key(
                [mod],
                str(i + 1),
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            # mod1 + shift + number of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                str(i + 1),
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
        ]
    )

layouts = [
    layout.Spiral(
        border_focus="#ECEFF4",
        border_normal="#3B4252",
        border_width=4,
        ratio=0.54,
        margin=inner_gap,
        new_client_position="bottom",
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Iosevka Nerd Font",
    foreground="#ECEFF4",
    background="#2E3440",
    fontsize=20,
    padding=0,
)
extension_defaults = widget_defaults.copy()

prompt = "{0}@{1}: ".format(environ["USER"], gethostname())


def separator(character="·", padding=9):
    return widget.TextBox(
        character,
        padding=padding,
        foreground="#5E6779",
    )


rect_decoration = decoration_group = {
    "decorations": [
        widget.decorations.RectDecoration(
            use_widget_background=True,
            radius=0,
            filled=True,
            padding_x=0,
            padding_y=4,
            clip=True,
        )
    ],
}

screens = [
    Screen(
        bottom=bar.Bar(
            [
                separator(character=" ", padding=3),
                widget.TextBox(
                    "Applications",
                ),
                separator(),
                widget.Volume(
                    fmt="Volume: <span color='{0}'>{1}</span>".format(
                        accent_color,
                        "{}",
                    )
                ),
                separator(),
                widget.Memory(
                    format="{MemUsed:.0f}M",
                    fmt="Memory: <span color='{0}'>{1}</span>".format(
                        accent_color, "{}"
                    ),
                ),
                widget.Prompt(prompt=prompt),
                widget.Spacer(bar.STRETCH),
                widget.GroupBox(
                    active="#ECEFF4",
                    inactive="#5E6779",
                    block_highlight_text_color="#2E3440",
                    this_current_screen_border=accent_color,
                    highlight_method="block",
                    rounded=False,
                    invert_mouse_wheel=True,
                    disable_drag=True,
                    border_width=0,
                    padding=15,
                    **rect_decoration,
                ),
                widget.Spacer(bar.STRETCH),
                widget.Clock(
                    format=f"%a, %b %d <span color='{accent_color}'>%H:%M</span>"
                ),
                separator(character=" ", padding=3),
            ],
            51,  # Bar height
            background="#2E3440",
            margin=[outer_gap, 0, 0, 0],
        ),
        top=bar.Gap(outer_gap),
        right=bar.Gap(outer_gap),
        left=bar.Gap(outer_gap),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
