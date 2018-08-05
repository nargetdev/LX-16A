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



AX_START=0x55
BROADCAST=0xFE
# TX_DELAY_TIME = 0.00002
TX_DELAY_TIME = 0.001

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

    def write_id(self, id, new_id):
        self.send_command(id, SERVO_ID_WRITE, [new_id])

    def ping_id(self):
        self.send_command(BROADCAST, SERVO_ID_READ, [])
        self.Serial_Con.flushInput()
        sleep(TX_DELAY_TIME)

        count=0
        sleep(0.1)
        while count<200:
            reply=self.Serial_Con.read(1)
            if reply != '':
                for x in range(0, 7):
                    #print reply.encode("hex"),
                    #print str(int(reply.encode("hex"),16))+""
                    if x == 5:
                        #print reply.encode("hex")
                        #print str(int(reply.encode("hex"),16))+"*C"
                        print("===")
                        id = int(reply.encode("hex"),16)
                        print(int(reply.encode("hex"),16))
                        print("===")
                    reply=self.Serial_Con.read(1)
                count=200
                #print("-----------")
                return id
            count+=1
            sleep(0.1)
