# DeathClicker

## Overview
DeathClicker is exactly what it sounds like. It counts how many "deaths" or tags a team has accrued during a match. When players respawn, they click the button on the box, which adds to the count.

## BOM
To make this, you will need: 
- 1x Pi Pico (link in root of this repo)
- 1x Button of choice (I used 60mm Arcade Buttons with the LEDS they came with): https://www.amazon.com/dp/B01M7PNCO9
- 1x I2C LCD Screen (https://www.amazon.com/dp/B0B76Z83Y4)
- 1x Low Profile Mechanical Switch (I used Gateron low profile yellows, but any low profile keyswitch will suffice): https://www.amazon.com/dp/B0CNGJ858B/
- 8x M3 Brass threaded inserts/"Heatsets": https://www.amazon.com/dp/B0CXXS3LHD
- Roughly 550 grams of your 3D Printer filament of your choice

## Wiring Guide/Pinout
### Buttons and LED
The clicker button is wired to GP0, and the LED is wired to GP13.
The reset button is wired to GP19.
### LCD Screen
The LCD Screen has its VCC wired to VBUS, the SCL pin wired to GP9, and the SDA pin wired to GP8.

## Libraries Used/Credits
This program uses Dean Halperts CircuityPython/LCD library.

https://github.com/dhalbert/CircuitPython_LCD

To use it, place the LCD folder on the root of your pi pico.

## Future Plans
### Modeling
Currently, I plan to create new versions of the box, embossed with RIT FBC's logo.
### Code
I plan to rewrite the code for this in C, so it can be compiled and easily flashed onto the pi pico.
