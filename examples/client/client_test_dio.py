#!/usr/bin/python3

from pprint import pprint
import time

from pytest_board_client.pin import Pin

# Set the path for the Unix socket

test_pin_in = Pin('/tmp/PIN8')
test_pin_out = Pin('/tmp/PIN9')

try:
    while True:
        print(test_pin_out.value)
        test_pin_in.value = not test_pin_in.value
        time.sleep(1)
except KeyboardInterrupt:
    print("now shutdown")
    test_pin_in.deinit()
    test_pin_out.deinit()

print("exit")
