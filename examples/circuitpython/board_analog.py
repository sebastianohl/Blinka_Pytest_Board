#!/usr/bin/python3

from os import environ

environ["BLINKA_PYTEST"] = "PYTEST"

print("Hello, blinka!")

import board
import analogio
import time

# Try to create a Digital input
test_pin_out = analogio.AnalogOut(board.D6)
test_pin_in = analogio.AnalogIn(board.D7)

value = 0.0
try:
    while True:
        time.sleep(1.0)
        value += 0.1
        test_pin_out.value = value
        print(test_pin_in.value)

except KeyboardInterrupt:
    test_pin_in.deinit()
    test_pin_out.deinit()

print("exit")
