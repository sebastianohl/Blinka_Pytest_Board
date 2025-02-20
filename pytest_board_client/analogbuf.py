from pytest_board_client.blinka import BlinkaConnection


class AnalogBuffer(BlinkaConnection):

    def __init__(
        self,
        socket_path,
    ):
        super().__init__(socket_path)
        self._buffer = []
        self._samplerate = None

    def deinit(self):
        return super().deinit()

    def _process(self, data):
        pass

    def __del__(self):
        return super().__del__()

    def senf_buffer_to(self, buf):
        self._send_packet({"type": "data", "value": buf})
