from pytest_board_client.blinka import BlinkaConnection
from enum import Enum
import PIL.Image
import struct
import base64


class ST7789(BlinkaConnection):

    class State(Enum):
        TWO_A = 1
        TWO_B = 2
        TWO_C = 3
        OTHER = 4

    def __init__(self,
                 socket_path,
                 new_image_callback=lambda x: 1 == 1,
                 width=280,
                 height=240):
        super().__init__(socket_path)
        self._width = width
        self._height = height
        self._new_image_callback = new_image_callback
        self._window = [[0, width], [0, height]]
        self._state = ST7789.State.OTHER
        self._im = PIL.Image.new(size=(self._width, self._height), mode="RGB")

    def deinit(self):
        return super().deinit()

    def __del__(self):
        return super().__del__()

    def _process(self, data):
        for d in data:
            raw_data = base64.b64decode(d['data'])
            if self._state == ST7789.State.TWO_A:
                self._state = ST7789.State.OTHER
                (_, self._window[0][0], _,
                 self._window[0][1]) = struct.unpack("BBBB", raw_data)
            if self._state == ST7789.State.TWO_B:
                self._state = ST7789.State.OTHER
                (self._window[1][0],
                 self._window[1][1]) = struct.unpack(">HH", raw_data)
            if self._state == ST7789.State.TWO_C:
                self._state = ST7789.State.OTHER
                self._to_image(raw_data)
            elif raw_data == b'\x2a':
                self._state = ST7789.State.TWO_A
            elif raw_data == b'\x2b':
                self._state = ST7789.State.TWO_B
            elif raw_data == b'\x2c':
                self._state = ST7789.State.TWO_C
            else:
                self._state = ST7789.State.OTHER

    def _to_image(self, data: bytes):
        counter = 0
        for counter in range(0, len(data), 2):
            bb = data[counter:counter + 2]

            pixel = struct.unpack(">H", bb)[0]
            R = ((pixel >> 13) & 0x1f) * (255 // 0x1f)
            G = ((pixel >> 5) & 0x3f) * (255 // 0x3f)
            B = ((pixel >> 1) & 0x1f) * (255 // 0x1f)
            x = self._window[0][0] + (counter // 2) // (self._window[0][1] -
                                                        self._window[0][0] + 1)
            y = self._window[1][0] + (counter // 2) % (self._window[0][1] -
                                                       self._window[0][0] + 1)
            if x < self._width and y < self._height:
                self._im.putpixel((x, self._height - y - 1), (R, G, B))
            counter += 1

        self._new_image_callback(self)

    def image(self):
        return self._im

    def set_callback(self, callback):
        self._new_image_callback = callback
