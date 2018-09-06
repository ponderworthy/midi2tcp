#!/usr/bin/env python
"""
Creates one JACK MIDI capture port.
Any MIDI messages received at that port, will be
sent to a pre-existing TCP server.

Example:
    python forward_ports.py localhost:44440

Assembled mostly from Mido library examples on Github.
"""
import sys
import time
import mido

server_host, tcp_port = mido.sockets.parse_address(sys.argv[1])
jack_port = mido.open_input()

try:
    with mido.sockets.connect(server_host, tcp_port) as server_port:
        print('Connected.')
#        print('Sending test note 0...')
#        testmessage = mido.Message('note_on', note=1, velocity=1, time=1)
#        server_port.send(testmessage)
#        testmessage = None
        for message in jack_port:
            # Skip inbound MIDI messages of type "clock" for now,
            # so we can study; a great many of them come from
            # some keyboard controllers
            if message.type == "clock":
                continue
            # Send the message inbound from JACK, to the RTP-MIDI server.
            server_port.send(message)
            print('Sent {}'.format(message))
            print('Timestamp ' + str(time.time()))
            print ('')

except KeyboardInterrupt:
    pass
