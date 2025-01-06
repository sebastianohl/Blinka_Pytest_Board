#!/usr/bin/python3

from os import environ

environ["BLINKA_PYTEST"] = "PYTEST"

print("Hello, blinka!")

import board
import terminalio
import displayio
import digitalio
import time

from fourwire import FourWire
from adafruit_display_text import label
from adafruit_st7789 import ST7789

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.CS
tft_dc = board.D0

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D1)

display = ST7789(display_bus, width=280, height=240, rowstart=0, rotation=90)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(135, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0,
                               y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(133, 238, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x0000FF
inner_sprite = displayio.TileGrid(inner_bitmap,
                                  pixel_shader=inner_palette,
                                  x=1,
                                  y=1)
splash.append(inner_sprite)

# Draw a label
text_group1 = displayio.Group(scale=2, x=20, y=40)
text1 = "PyTest"
text_area1 = label.Label(terminalio.FONT, text=text1, color=0xFF0000)
text_group1.append(text_area1)  # Subgroup for text scaling
# Draw a label
text_group2 = displayio.Group(scale=1, x=20, y=60)
text2 = "CircuitPython"
text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF)
text_group2.append(text_area2)  # Subgroup for text scaling

# Draw a label
text_group3 = displayio.Group(scale=1, x=20, y=100)
text3 = ST7789.__name__
text_area3 = label.Label(terminalio.FONT, text=text3, color=0x0000000)
text_group3.append(text_area3)  # Subgroup for text scaling
# Draw a label

splash.append(text_group1)
splash.append(text_group2)
splash.append(text_group3)

try:
    rot = 0
    while True:
        time.sleep(1.0)
        print("rotate")
        rot = rot + 90
        if (rot >= 360):
            rot = 0
        display.rotation = rot

except KeyboardInterrupt:
    spi.deinit()

print("exit")
