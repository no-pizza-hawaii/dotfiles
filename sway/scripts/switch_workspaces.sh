#!/usr/bin/env bash

# Getting all outputs
# external_outputs=$(swaymsg -rt get_outputs | jq '.[].name | select(. != "eDP-1")')
external_outputs=("HDMI-A-1" "DP-1")
workspaces=$(swaymsg -rt get_workspaces)

for index in "${!external_outputs[@]}"; do
    output="${external_outputs[$index]}"
    workspace=$(echo "$workspaces" | jq '.[]|select(.visible == true and .output == "'$output'").num')
    new_index=$(($((index + 1)) % "${#external_outputs[@]}"))
    new_output="${external_outputs[$new_index]}"
    swaymsg workspace ${workspace}
    swaymsg move workspace to output ${new_output}
    echo "Index: $index, Output: $output, Workspace: $workspace -> $new_index ($new_output)"
done
