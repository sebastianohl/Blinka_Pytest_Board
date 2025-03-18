from pytest_board_client.blinka import BlinkaConnection


class Pin(BlinkaConnection):

    # pin modes
    OUT = 0
    IN = 1
    ADC = 2
    DAC = 3
    # pin values
    LOW = 0
    HIGH = 1
    # pin pulls
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2

    def __init__(
        self,
        socket_path,
        new_data_callback=lambda x: 1 == 1,
    ):
        super().__init__(socket_path)
        self._mode = None
        self._pull = None
        self._current_value = None
        self._new_data_callback = new_data_callback

    def deinit(self):
        return super().deinit()

    def __del__(self):
        return super().__del__()

    def _process(self, data):
        for d in data:
            if d['type'] == "config":
                self._mode = d['data']['mode']
                self._pull = d['data']['pull']
            elif d['type'] == "data":
                self._current_value = d['value']
        self._new_data_callback(self)

    @property
    def value(self):
        # is pin a pull up and pin is LOW?
        if self._pull == Pin.PULL_UP and self._current_value is False:
            self._current_value = False
        # is pin a pull down and pin is HIGH?
        if self._pull == Pin.PULL_DOWN and self._current_value is True:
            self._current_value = False
        return self._current_value

    @value.setter
    def value(self, v):
        self._current_value = v
        if self._pull == Pin.PULL_UP and self._current_value is False:
            self._current_value = False
        # is pin a pull down and pin is HIGH?
        if self._pull == Pin.PULL_DOWN and self._current_value is True:
            self._current_value = False

        self._send_packet({"value": self._current_value})

    def set_callback(self, callback):
        self._new_data_callback = callback
