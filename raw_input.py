from time import sleep
from serial import Serial
from LX_16a import LX_16a


import os
import multiprocessing
import threading

import json

SCAN_RANGE=16


lx = LX_16a() # the lx-16a bus

LX_ID0 = 1
sleepytime=0.5

while(1):
    command = None
    try:
        command = raw_input("Command? (or 'help')")
    except Exception as error:
        print(error)
        continue

    print(command)
    # if command == 'p':
    #     lx.ping_scan()
