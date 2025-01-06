#!/usr/bin/python3

from os import environ

environ["BLINKA_PYTEST"] = "PYTEST"

print("Hello, blinka!")

import board
import terminalio
import displayio
import digitalio
import time

# Try to create a Digital input
test_pin_out = digitalio.DigitalInOut(board.D9)
test_pin_out.switch_to_output()
test_pin_in = digitalio.DigitalInOut(board.D8)
test_pin_in.switch_to_input()
print("Digital IO ok!")

try:
    while True:
        time.sleep(1.0)
        test_pin_out.value = not test_pin_out.value
        print(test_pin_in.value)

except KeyboardInterrupt:
    test_pin_in.deinit()
    test_pin_out.deinit()

print("exit")
