from time import sleep
from serial import Serial

dictErrors = {  1 : "Input Voltage",
                2 : "Angle Limit",
                4 : "Overheating",
                8 : "Range",
                16 : "Checksum",
                32 : "Overload",
                64 : "Instruction"
}

AX_START=0x55
TX_DELAY_TIME = 0.00002

class LX_16a():

    Serial_Con = None

    def __init__(self):
        print("trying to connect")
        try:
            self.Serial_Con = Serial("/dev/ttyUSB0", baudrate=115200, timeout=0.001)
            self.Serial_Con.setDTR(1)
        except Exception as e:
            print(e)
            print("failed to connect")
        print("initialized")

    def write_position(self, id, speed, position):
        #print("Moving Servo ID:"+str(id)+"----------------------")
        AX_REG_WRITE =1
        AX_GOAL_SP_LENGTH =7
        if(position < 0):
            position = 0
        if(position > 1000):
            position = 1000
        if(speed < 0):
            speed = 0
        if(speed > 30000):
            speed = 30000

        p = [position&0xff, position>>8]
        s = [speed&0xff, speed>>8]
        checksum = (~(id + AX_GOAL_SP_LENGTH + AX_REG_WRITE + p[0] + p[1] + s[0] + s[1]))&0xff
        outData = chr(AX_START)
        #print(hex(ord(chr(AX_START))))
        outData += chr(AX_START)
        #print(hex(ord(chr(AX_START))))
        outData += chr(id)
        #print(hex(ord(chr(id))))
        outData += chr(AX_GOAL_SP_LENGTH)
        #print(hex(ord(chr(AX_GOAL_SP_LENGTH))))
        outData += chr(AX_REG_WRITE)
        #print(hex(ord(chr(AX_REG_WRITE))))
        outData += chr(p[0])
        #print(hex(ord(chr(p[0]))))
        outData += chr(p[1])
        #print(hex(ord(chr(p[1]))))
        outData += chr(s[0])
        #print(hex(ord(chr(s[0]))))
        outData += chr(s[1])
        #print(hex(ord(chr(s[1]))))
        outData += chr(checksum)
        #print(hex(ord(chr(checksum))))
        self.Serial_Con.write(outData)
        sleep(TX_DELAY_TIME)
        return True
    #print("Done -----------")
