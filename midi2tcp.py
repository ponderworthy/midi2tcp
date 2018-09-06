#!/usr/bin/env python
"""
Creates one MIDI capture port, and
connects to a prestarted TCP server.
Any MIDI messages received at the MIDI port, will be
sent to the TCP server.

Example:
    python midi2tcp.py localhost:44440

Assembled mostly from Mido library examples on Github.
"""
import sys
import time
import mido

if len(sys.argv) <= 1:
    print('Usage: python[2] midi2tcp.py hostname:44440]')
    exit(0)

jack_port = mido.open_input('tcp2midi', virtual=True)

server_host, tcp_port = mido.sockets.parse_address(sys.argv[1])

try:
    with mido.sockets.connect(server_host, tcp_port) as server_port:
        print('Connected.')
        while True:
            # Wait for message to arrive via the JACK port
            message = jack_port.receive()
            server_port.send(message)
            # Don't report MIDI messages of type "clock",
            # a great many of them come from some keyboard controllers
            if message.type == "clock":
                continue
            print('Message received from JACK: ' + message.type)
            server_port.send(message)
            print('Sent {}'.format(message))
            print('Timestamp ' + str(time.time()))
            print ('')

except KeyboardInterrupt:
    pass
