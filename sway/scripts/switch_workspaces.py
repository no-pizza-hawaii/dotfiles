#!/usr/bin/python

import subprocess
import json

command = "swaymsg -rt get_outputs | jq '.[].name | select(. != \"eDP-1\")'"
process = subprocess.Popen(
    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
data = json.loads(process.communicate()[0])
outputs = 

# for i, output in enumerate(outputs):
    # workspace = subprocess.