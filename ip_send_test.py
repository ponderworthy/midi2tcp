
import sys
import mido
from mido.sockets import PortServer, connect

output = connect('localhost', 44440)
message = mido.Message('note_on', note=100, velocity=3, time=1)
output.send(message)
