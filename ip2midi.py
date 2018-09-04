#!/usr/bin/env python
"""
Creates a TCP server and one JACK MIDI playback port.
Every message received by the TCP server, will be sent to
the one JACK MIDI port.

Example:
    python serve_ports.py localhost:44440

Assembled mostly from Mido library examples on Github.
"""
import sys
import time
import mido
from mido import sockets

jackport = mido.open_output()

(host, port) = sockets.parse_address(sys.argv[1])

try:
    with sockets.PortServer(host, port) as server:
        for message in server:
            print('Received {}'.format(message))
            print('Timestamp ' + str(time.time()))
            print ('')
            jackport.send(message)

except KeyboardInterrupt:
    pass
