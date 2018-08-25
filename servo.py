from time import sleep
from serial import Serial
from LX_16a import LX_16a


import os
import multiprocessing
import threading

import json

SCAN_RANGE=16



def watch_ids():
    """ Do some computations """
    print("PID: %s, Process Name: %s, Thread Name: %s" % (
        os.getpid(),
        multiprocessing.current_process().name,
        threading.current_thread().name)
    )
    print("checking for one")
    try:
        lx.check_and_allocate()
    except:
        "something wrong"
    threading.Timer(3, watch_ids).start()



print("yo dawg.")

lx = LX_16a() # the lx-16a bus

# watch_ids_thread = threading.Thread(target=watch_ids)
# watch_ids_thread.start()

# lx.write_position(2, 100, 0)
# lx.write_position(3, 100, 1000)
# sleep(1)


# for i in range(1, SCAN_RANGE):
#     print("i: " + str(i) + " Present? " + str(lx.ping_id(i) ) )

lx.ping_scan()

LX_ID0 = 1
sleepytime=0.1





while(1):
    print("write positions")

    for j in xrange(10):
        print(j)
        for i in xrange(2, 15):
            lx.write_position(i, 100, j*100)
        sleep(sleepytime)