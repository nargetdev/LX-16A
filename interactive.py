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
    try:
        input("Enter an expression...\n")
    except Exception as error:
        print(error)
        continue
    # if command == 'p':
    #     lx.ping_scan()
