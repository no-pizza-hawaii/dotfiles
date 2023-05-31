#!/bin/bash

# get formatted player metadata from mediaplayer.py
# run wofi with this data
# get everything in between <i> and </i> (player name)
# toggle play/pause of this player
selected=$($HOME/.config/waybar/scripts/mediaplayer.py --metadata | wofi --conf=$HOME/.config/wofi/config.media --style=$HOME/.config/wofi/style.css | awk -F'<(/?)i>' '{print $2}')
playerctl play-pause -p $selected
