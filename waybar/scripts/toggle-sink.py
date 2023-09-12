#!/usr/bin/python3

import subprocess
import re

# Check if bluetooth is connected and get MAC
try:
    bluetooth_connected = subprocess.check_output(["bluetoothctl", "player.list"], timeout=0.1)
    pattern = b'[0-9a-fA-F]{2}(_[0-9a-fA-F]{2}){5}'
    match = re.search(pattern, bluetooth_connected)
    if match:
        mac = match.group()
        bluetooth_connected = f"bluez_output.{mac.decode()}.1"
    else:
        bluetooth_connected = None
except:
    bluetooth_connected = None

current = subprocess.check_output(["pactl", "get-default-sink"])
if b"SteelSeries" in current and bluetooth_connected:
    subprocess.call(["pactl", "set-default-sink", bluetooth_connected])
elif b"SteelSeries" in current or b"bluez_output" in current:
    subprocess.call(["pactl", "set-default-sink", "alsa_output.pci-0000_00_1f.3.analog-stereo"])
else:
    subprocess.call(["pactl", "set-default-sink", "alsa_output.usb-SteelSeries_SteelSeries_Arctis_5_00000000-00.analog-game"])

