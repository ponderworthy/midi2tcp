#!/usr/bin/env python
"""
Creates a TCP server and one JACK MIDI playback port.
Every message received by the TCP server, will be sent to
the one JACK MIDI port.

Example:
    python tcp2midi.py localhost:44440

Assembled mostly from Mido library examples on Github.
"""
import sys
import time
import mido
from mido import sockets

if len(sys.argv) <= 1:
    print('Usage: python[2] tcp2midi.py hostname:44440')
    exit(0)

(host, port) = sockets.parse_address(sys.argv[1])

jack_port = mido.open_output('tcp2midi', virtual=True)

try:
    with sockets.PortServer(host, port) as server:
        print('TCP server prepared and waiting...')
        for message in server:
            jack_port.send(message)
            # Don't report MIDI messages of type "clock",
            # a great many of them come from some keyboard controllers
            if message.type == "clock":
                continue
            print('Received {}'.format(message))
            print('Timestamp ' + str(time.time()))
            print ('')

except KeyboardInterrupt:
    pass
