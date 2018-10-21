import random
import socket

import time

from struct import *

from LX_16a import LX_16a

lx = LX_16a() # the lx-16a bus

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 2345))

lx.ping_scan()

print("Expecting 24 motors worth of half words.")
while True:
    message, address = server_socket.recvfrom(1024)
    print("========")
    try:
        for i, intval in enumerate(unpack('24h', message)):
            print('before')
            cmd_id = lx.get_id(i)
            print(cmd_id, intval)
            # lx.write_position(cmd_id, 50, intval)
            lx.write_effort_spool(cmd_id, intval)
    except Exception as e:
        print(len(message))
        print("fuck", e)
        time.sleep(0.1)
    # message = message.upper()
    # if rand >= 4:
    #     server_socket.sendto(message, address)