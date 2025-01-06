#!/usr/bin/python3

from pprint import pprint
import time

from pytest_board_client.pin import Pin

# Set the path for the Unix socket

test_pin_in = Pin('/tmp/PIN7')
test_pin_out = Pin('/tmp/PIN6')

value = 0.0
try:
    while True:
        value += 0.1
        print(test_pin_out.value)
        test_pin_in.value = value
        time.sleep(1)
except KeyboardInterrupt:
    print("now shutdown")
    test_pin_out.deinit()
    test_pin_in.deinit()

print("exit")
