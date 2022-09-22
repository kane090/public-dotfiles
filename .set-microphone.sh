#!/bin/bash
pactl set-default-source 'alsa_input.pci-0000_00_1f.3.analog-stereo'
pactl set-source-volume @DEFAULT_SOURCE@ 19661
