# Images
All Images found on google / google-earth-pro.

# Script
I have written this script for my personal use as I often change my wallpapers around to match my work setting.
It uses pywal to generate colorprofiles for my urxvt terminal based on the selected wallpaper.
Apart from that it only allows you to search through the images in a folder and choose one to use as new wallpaper / default wallpaper / flip through neighbouring images to use as wallpaper.

## Requirements
https://github.com/dylanaraps/pywal

## Usage
```shell
/path/to/repo$ python3 bgswap -h
bgswap (-l|--list) [-v]   List all available wallpapers.
bgswap (-s|--set)  [NUM]  Set wallpaper (to NUM).
bgswap (-d|--def)  [NUM]  Set default (to NUM).
bgswap (-r|--reset)       Reset to default.
bgswap (-c|--curr)        Print current wallpaper.
bgswap (-n|--next)        Switch wallpaper to next.
bgswap (-p|--prev)        Switch wallpaper to previous.
bgswap (-h|--help)        Print this help message.
```

### Selecting options
```shell
/path/to/repo$ python3 bgswap -s
[...]
71: library.jpg
72: anime/light_spirited_away_train.png
73: anime/light_city_tokyo_hinamatsuri.png
74: anime/dark_city_tokyo_tokyoghoul.png
75: akira/awaken_akira_circle_28.PNG
76: akira/awaken_akira_dark_city.PNG
77: akira/awaken_akira_gate.PNG
78: akira/awaken_akira_lights.PNG
79: akira/awaken_akira_red.PNG
80: akira/awaken_akira_light_B1.PNG
81: akira/awaken_akira.PNG

Set wallpaper to number: _
```

Either specify search terms to reduce the results:
```shell
Set wallpaper to number: akira<Enter>
75: akira/awaken_akira_circle_28.PNG
76: akira/awaken_akira_dark_city.PNG
77: akira/awaken_akira_gate.PNG
78: akira/awaken_akira_lights.PNG
79: akira/awaken_akira_red.PNG
80: akira/awaken_akira_light_B1.PNG
81: akira/awaken_akira.PNG

Set wallpaper to number: _
```

Or specify the number:
```shell
Set wallpaper to number: 76<Enter>
[I] image: Using image /home/omni/bgswap/akira/awaken_akira_dark_city.PNG
[...]

```

Or abort:
```shell
Set wallpaper to number: <Enter>
Exit.
```

## Default and Current
The script will generate files to store the path of the wallpaper that was last set (`.current`) and the wallpaper that was set to the default with the `-d` option (`.default`).

## Next and Previous Image
You can flip through the images by using the `-n|--next` and `-p|--prev` flags.

## Binding to i3
You can add the following lines to your `~/.config/i3/config`:

```
# Hotkey for next wallpaper
bindsym $mod+m exec bgswap --next

# Hotkey for previous wallpaper
bindsym $mod+n exec bgswap --prev

# Auto set default on start (Need to set default with 'bgswap -d [num]')
exec bgswap -r
```

Don't forget to add the script to your path and making it executable.
(E.g.: `echo -e '#!/bin/bash\npython3 ~/bgswap/bgswap.py "$@"' > /usr/local/bin/bgswap`)

