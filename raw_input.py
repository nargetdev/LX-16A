from time import sleep
from serial import Serial
from LX_16a import LX_16a

import sys


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
        command = raw_input("Command? (or 'help')\n")
        # command = screen.getch()
    except Exception as error:
        print(error)
        continue

    # print(command)
    if command == 'w':
        print("hoha")
        lx.wiggle(3)

    if command=='\x1b[A':
            print "up"
    elif command=='\x1b[B':
            print "down"
    # if command == 'p':
    #     lx.ping_scan()
