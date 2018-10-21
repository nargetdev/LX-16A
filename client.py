import random
import socket

from struct import *

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
Message = "Hello, Server"

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clientSock.sendto(Message, (UDP_IP_ADDRESS, UDP_PORT_NO))

twelve = range(12)
var = pack('12h', twelve)
print(var)

# print("Expecting 12 motors worth of half words.")
# while True:
#     rand = random.randint(0, 10)
#     message, address = server_socket.recvfrom(1024)
#     try:
#         for i, intval in enumerate(unpack('12h', message)):
#             cmd_id = lx.get_id(i)
#             print(cmd_id, intval)
#             lx.write_position(cmd_id, 50, intval)
#     except Exception as e:
#         print("fuck", e)
#     # message = message.upper()
#     # if rand >= 4:
#     #     server_socket.sendto(message, address)