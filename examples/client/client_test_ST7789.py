#!/usr/bin/python3

from pprint import pprint
import time

from pytest_board_client.st7789 import ST7789
from pytest_board_client.pin import Pin

# Set the path for the Unix socket

st7789 = ST7789('/tmp/SPI0', lambda x: x.image().save("test.png"))

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("now shutdown")
    st7789.deinit()

print("exit")
