# KOTH

## Overview
KOTH stands for King Of The Hill. The objective of this game is to "control" an objective for a period of time before your opponents can do the same. This timer also has the "Death Clicker" game mode built in, and can swap from KOTH and Death Clicks using the "Mode" button.

## BOM
To Make this, you will need:

- 1x Pi Pico (Link in readme in root of this repo)
- 2x Button of Choice (I used the same 60mm arcade buttons from DeathClicker and the LEDS they came with): https://www.amazon.com/dp/B01M7PNCO9
- 1x I2C screen: https://www.amazon.com/dp/B0B76Z83Y4
- 4x Low Profile Mechanical Switches: https://www.amazon.com/dp/B0CNGJ858B/
- 8x M3 Brass Threaded "Heatset" inserts: https://www.amazon.com/dp/B0CXXS3LHD
- 8x M3 Socket Cap Screws: https://www.amazon.com/dp/B083SGJ7BD/
- Roughly 550 Grams of 3D printer filament of your choice

## Wiring Guide

Red Button: GP21

Blue Button: GP22

SCL: GP9

SDA: GP8

Mode: GP18

Time Up: GP15

Time Down: GP13

Red LED: GP28

Blue LED: GP27

Reset Button: GP16

## Libraries Used/Credits

This program uses Dean Halperts CircuityPython/LCD library.

https://github.com/dhalbert/CircuitPython_LCD

To use it, place the LCD folder on the root of your pi pico.
