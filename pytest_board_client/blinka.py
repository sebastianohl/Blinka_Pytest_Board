from pprint import pprint

import socket
import json

from threading import Thread, Event
from queue import Queue
from select import select

break_threads = Event()


def spi_socket(blinka):
    buffer = ''
    while not break_threads.is_set():
        # Receive a response from the server
        r, w, x = select([blinka._client, blinka._thread_fd], [], [], 1.0)
        if break_threads.is_set():
            break

        if blinka._client in r:
            response = blinka._client.recv(100000)
            if len(response) == 0:
                break
            buffer += response.decode()
            #print(
            #    f'Received response: {len(response)} / {len(buffer)} / {buffer[0:5]} {buffer[-5:]}'
            #)
            data, buffer = blinka._extract_json_objects(buffer)
            #print(f"got {len(data)} objects {len(buffer)}")
            blinka._process(data)

        if blinka._thread_fd in r:
            blinka._thread_fd.recv(100)  # clear pipe
            while not blinka._outgoing.empty():
                #print("send data")
                data = json.dumps(blinka._outgoing.get())
                blinka._client.sendall(data.encode())

    print(f"shutting blinka thread {blinka._socket_path}")


class BlinkaConnection():

    def __init__(self, socket_path):
        # Set the path for the Unix socket
        self._socket_path = socket_path

        self._outgoing = Queue()
        (self._child_fd, self._thread_fd) = socket.socketpair(socket.AF_UNIX)
        self._thread = Thread(target=spi_socket, args=(self, ))

        # Create the Unix socket client
        self._client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        # Connect to the server
        self._client.connect(self._socket_path)
        self._thread.start()

    def deinit(self):
        break_threads.set()
        self._child_fd.send("shutdown".encode())
        self._thread.join()
        if self._client is not None:
            # Close the connection
            self._client.close()

    def __del__(self):
        self.deinit()

    def _send_packet(self, packet):
        """Write data via socket"""

        self._outgoing.put(packet)
        self._child_fd.send("data is here".encode())

    def _process(self, data):
        assert False, "please implement _process()"

    def _extract_json_objects(self, text, decoder=json.JSONDecoder()):
        """Find JSON objects in text, and yield the decoded JSON data

        Does not attempt to look for JSON arrays, text, or other JSON types outside
        of a parent JSON object.

        Source: https://stackoverflow.com/questions/54235528/how-to-find-json-object-in-text-with-python, 2025-01-03
        """
        pos = 0
        data = []
        while True:
            match = text.find('{', pos)
            if match == -1:
                break
            try:
                result, index = decoder.raw_decode(text[match:])
                data.append(result)
                pos = match + index
            except ValueError:
                pos = match
                break
        return data, text[pos:]
