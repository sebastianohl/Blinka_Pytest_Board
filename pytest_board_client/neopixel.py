class NeoPixel:
    # Pixel color order constants
    RGB = "RGB"
    """Red Green Blue"""
    GRB = "GRB"
    """Green Red Blue"""
    RGBW = "RGBW"
    """Red Green Blue White"""
    GRBW = "GRBW"
    """Green Red Blue White"""

    def __init__(self,
                 pin,
                 number_of_pixel,
                 pixel_order,
                 new_data_callback=lambda neopixel, idx, px: 1 == 1):
        self._pin = pin
        self._number_of_pixel = number_of_pixel
        self._pixel_order = pixel_order
        self._new_data_callback = new_data_callback

        self._pin.set_callback(self._process)

        self._pixel = [[None, None, None, None]] * self._number_of_pixel

    def deinit(self):
        return self._pin.deinit()

    def _process(self, pin):
        idx = 0
        v = pin.value
        for px in self._pixel:
            px[0] = v[idx]
            px[1] = v[idx + 1]
            px[2] = v[idx + 2]
            px[3] = v[idx + 3]
            idx += 4
            self._new_data_callback(self, idx // 4 - 1, px)

    def pixel(self, idx):
        assert idx < self._number_of_pixel, "idx to large"

        return self._pixel[idx]
