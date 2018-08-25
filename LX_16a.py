from time import sleep
from serial import Serial
import json
import signal
from shutil import copyfile
from array import array

import pickle

dictErrors = {  1 : "Input Voltage",
                2 : "Angle Limit",
                4 : "Overheating",
                8 : "Range",
                16 : "Checksum",
                32 : "Overload",
                64 : "Instruction"
}

SERVO_MOVE_TIME_WRITE=[1, 7]
SERVO_MOVE_TIME_READ=[2, 3]
SERVO_MOVE_TIME_WAIT_WRITE=[7, 7]
SERVO_MOVE_TIME_WAIT_READ=[8, 3]
SERVO_MOVE_START=[11, 3]
SERVO_MOVE_STOP=[12, 3]
SERVO_ID_WRITE=[13, 4]
SERVO_ID_READ=[14, 3]
SERVO_ANGLE_OFFSET_ADJUST=[17, 4]
SERVO_ANGLE_OFFSET_WRITE=[18, 3]
SERVO_ANGLE_OFFSET_READ=[19, 3]
SERVO_ANGLE_LIMIT_WRITE=[20, 7]
SERVO_ANGLE_LIMIT_READ=[21, 3]
SERVO_VIN_LIMIT_WRITE=[22, 7]
SERVO_VIN_LIMIT_READ=[23, 3]
SERVO_TEMP_MAX_LIMIT_WRITE=[24, 4]
SERVO_TEMP_MAX_LIMIT_READ=[25, 3]
SERVO_TEMP_READ=[26, 3]
SERVO_VIN_READ=[27, 3]
SERVO_POS_READ=[28, 3]
SERVO_OR_MOTOR_MODE_WRITE=[29, 7]
SERVO_OR_MOTOR_MODE_READ=[30, 3]
SERVO_LOAD_OR_UNLOAD_WRITE=[31, 4]
SERVO_LOAD_OR_UNLOAD_READ=[32, 3]
SERVO_LED_CTRL_WRITE=[33, 4]
SERVO_LED_CTRL_READ=[34, 3]
SERVO_LED_ERROR_WRITE=[35, 4]
SERVO_LED_ERROR_READ=[36, 3]


SCAN_RANGE=16



AX_START=0x55
BROADCAST=0xFE
# TX_DELAY_TIME = 0.00002
TX_DELAY_TIME = 0.001

class LX_16a():

    min_id = 2
    max_id = 15

    sel_id = min_id

    ids = range(min_id, max_id + 1)

    spool_direction = {}

    id_idx = 0
    cur_id = 0


    UPPER_BOUND = 999
    LOWER_BOUND = -UPPER_BOUND

    Serial_Con = None
    registered_ids = {}
    non_volatile_id_counter = None # this variable will hold the next *available* id for assignment

    def __init__(self):
        print("trying to connect")
        try:
            self.Serial_Con = Serial("/dev/ttyUSB0", baudrate=115200, timeout=0.001)
            self.Serial_Con.setDTR(1)
        except Exception as e:
            print(e)
            print("failed to connect")
        print("initialized")
        print("loading non_volatile_id_counter")
        with open('.id_counter', 'r') as f:
            self.non_volatile_id_counter = json.load(f)
        print(self.non_volatile_id_counter)

        # section gets the polarities we consider positive on the bus.
        print("loading non_volatile polarities")
        filename = "polarities"
        try:
            with open(filename,'r') as fileObject:
                # this writes the object a to the
                # file named 'testfile'
                self.spool_direction = pickle.load(fileObject)   
        except:
            print("polarities probably doesn't exist yet")
        for id in self.ids:
            if not id in self.spool_direction:
                print("making new initialization for spool")
                self.spool_direction[id] = 0
        print(self.spool_direction)


    def next_id(self, rotate):
        new_idx = self.id_idx + rotate
        if new_idx >= len(self.ids):
            new_idx = 0
        elif new_idx <= -1:
            new_idx = len(self.ids) - 1
        id_idx = new_idx
        # print("id: " + str(ids[id_idx]) + "idx: " + str(id_idx))
        self.cur_id = self.ids[id_idx]
        return self.ids[id_idx]

    def get_id(self, id_idx):
        return self.ids[id_idx]

    def checksum(self, id, cmd, params):
        LENGTH = cmd[1]
        sum = 0
        sum += id
        sum += cmd[1] + cmd[0]
        for arg in params:
            sum += arg
        return (~(sum))&0xff

    def send_command(self, id, CMD, params):
        checksum = self.checksum(id, CMD, params)
        outData = chr(AX_START)
        outData += chr(AX_START)
        outData += chr(id)
        outData += chr(CMD[1]) # Length
        outData += chr(CMD[0]) # Command
        for arg in params:
            outData += chr(arg)
        outData += chr(checksum)
        self.Serial_Con.write(outData)
        sleep(TX_DELAY_TIME)

    def set_polarity(self, id, polarity):
        self.spool_direction[id] = polarity

        filename = "polarities"
        with open(filename,'wb') as fileObject:
            # this writes the object a to the
            # file named 'testfile'
            pickle.dump(self.spool_direction,fileObject)   
        print("CURRENT:")
        print(self.spool_direction)


    # same as write effort below except only accepts values 0 - 999 and only lets spools exist in tension
    def write_effort_spool(self, id, effort):
        assert(effort >= 0)
        effort *= self.spool_direction[id] # a 1 if spool rotation should be counter clockwise a -1 if should be clockwise
        self.write_effort(id, effort)

    def write_effort(self, id, effort):
        p1_mode = 1 # this is wheel mode, 0 is position control mode
        p2_null = 0 # second param is null for some reason
        p3_effort_lo = effort & 0xff
        p4_effort_hi = effort >> 8

        # template for constructing the signed int bytes.
        a = array("h")

        self.send_command(id, SERVO_OR_MOTOR_MODE_WRITE, [p1_mode, p2_null, p3_effort_lo, p4_effort_hi])

    def position_mode(self, id):
        p1_mode = 0 # this is wheel mode, 0 is position control mode
        p2_null = 0 # second param is null for some reason
        p3_speed_lo = 0
        p4_speed_hi = 0
        self.send_command(id, SERVO_OR_MOTOR_MODE_WRITE, [p1_mode, p2_null, p3_speed_lo, p4_speed_hi])
        
    def torque_enable(self, id, enable):
        self.send_command(id, SERVO_LOAD_OR_UNLOAD_WRITE, [enable])


    def read_pos(self, id):
        #read command
        self.send_command(id, SERVO_POS_READ, [])

        # get the response
        count = 0
        while count<200:
            reply=self.Serial_Con.read(1)
            if reply != '':
                for x in range(0, 8):
                    #print reply.encode("hex"),
                    #print str(int(reply.encode("hex"),16))+""
                    if x == 5:
                        #print reply.encode("hex")
                        #print str(int(reply.encode("hex"),16))+"*C"
                        pos1=reply.encode("hex")
                    if x == 6:
                        #print reply.encode("hex")
                        #print str(int(reply.encode("hex"),16))+"*C"
                        pos2=int(reply.encode("hex")+pos1,16)
                    reply=self.Serial_Con.read(1)
                count=200
                #print("-----------")
                return pos2
            count+=1
            sleep(0.1)


    def write_position(self, id, speed, position):
        if position < 0:
            position = 0
        if position > 1000:
            position = 1000
        if speed < 0:
            speed = 0
        if speed > 30000:
            speed = 30000

        p = [position&0xff, position>>8]
        s = [speed&0xff, speed>>8]
        self.send_command(id, SERVO_MOVE_TIME_WRITE, [p[0], p[1], s[0], s[1]])
        return True

    def write_id(self, new_id, id=1):
        self.send_command(id, SERVO_ID_WRITE, [new_id])

    def limit_bounds(self, cmd):
        if cmd >= self.UPPER_BOUND:
            return self.UPPER_BOUND
        elif cmd <= self.LOWER_BOUND:
            return self.LOWER_BOUND
        else:
            return cmd

    def ping_id(self, id=None):
        if id:
            self.send_command(id, SERVO_ID_READ, [])
        else:
            self.send_command(BROADCAST, SERVO_ID_READ, [])
        self.Serial_Con.flushInput()
        sleep(TX_DELAY_TIME)

        count=0
        while count<16:
            reply=self.Serial_Con.read(1)
            if reply != '':
                for x in range(0, 7):
                    #print reply.encode("hex"),
                    #print str(int(reply.encode("hex"),16))+""
                    if x == 5:
                        #print reply.encode("hex")
                        #print str(int(reply.encode("hex"),16))+"*C"
                        # print("===")
                        id = int(reply.encode("hex"),16)
                        # print(int(reply.encode("hex"),16))
                        # print("===")
                    reply=self.Serial_Con.read(1)
                count=200
                #print("-----------")
                return id
            count+=1
            # sleep(0.1)

    def check_and_allocate(self):
        print("NEXT QUEUED: " + str(self.non_volatile_id_counter))
        print("checking 1")
        if self.ping_id(1) == 1:
            print("found 1 needs reallocate")
            print("allocating id: " + str(self.non_volatile_id_counter))
            self.write_id(self.non_volatile_id_counter)
            self.non_volatile_id_counter += 1
            print("writing next available id to '.id_counter': " + str(self.non_volatile_id_counter))
            with open('.id_counter.tmp', 'w+') as f:
                json.dumps(str(self.non_volatile_id_counter), f)

            copyfile('.id_counter.tmp', '.id_counter')
        else:
            print("one not found, doing nothing")

        print("ids on the bus now: ")
        self.ping_scan()

    def ping_scan(self):
        for i in range(1, SCAN_RANGE):
            print("i: " + str(i) + " Present? " + str(self.ping_id(i) ) )
                
    def wiggle(self, id):
        WIGGLE_NUM = 2
        sleepytime = .1
        for i in range(1, WIGGLE_NUM):
            # print("wiggling id " + str(id))
            self.write_position(id, 50, 0)
            sleep(sleepytime)
            self.write_position(id, 50, 100)
            sleep(sleepytime)
                
    def increment_position(self, id):
        cur_pos = self.read_pos(id)
        cmd_pos = cur_pos + 100
        if cmd_pos > 1023:
            cmd_pos = 1023
        self.write_position(id, 100, cmd_pos)

    def decrement_position(self, id):
        cur_pos = self.read_pos(id)
        cmd_pos = cur_pos - 100
        if cmd_pos < 0:
            cmd_pos = 0
        self.write_position(id, 100, cmd_pos)
                


