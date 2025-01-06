#!/usr/bin/python3

from pprint import pprint
import time

from pytest_board_client.pin import Pin
from pytest_board_client.neopixel import NeoPixel

# Set the path for the Unix socket

test_pin_neopixel = Pin('/tmp/PIN2')
np = NeoPixel(pin=test_pin_neopixel,
              number_of_pixel=1,
              pixel_order=NeoPixel.GRB,
              new_data_callback=lambda np, px, idx: print([idx, px]))

try:
    while True:
        #print(np.pixel(0))
        time.sleep(1)
except KeyboardInterrupt:
    print("now shutdown")
    test_pin_neopixel.deinit()

print("exit")
