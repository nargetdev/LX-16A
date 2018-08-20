def ReadTemp(id):
    #print("Read Temp ID:"+str(id)+"-------------")
    AX_READ_DATA=3
    AX_TEMP_READ=26
    Serial_Con.flushInput()
    checksum = (~(id + AX_READ_DATA + AX_TEMP_READ))&0xff
    outData = chr(AX_START)
    #print(hex(ord(chr(AX_START))))
    outData += chr(AX_START)
    #print(hex(ord(chr(AX_START))))
    outData += chr(id)
    #print(hex(ord(chr(id))))
    outData += chr(AX_READ_DATA)
    #print(hex(ord(chr(AX_READ_DATA))))
    outData += chr(AX_TEMP_READ)
    #print(hex(ord(chr(AX_TEMP_READ))))
    outData += chr(checksum)
    #print(hex(ord(chr(checksum))))
    Serial_Con.write(outData)
    sleep(TX_DELAY_TIME)
    #print("Done -----------")
    count=0
    sleep(0.1)
    while count<200:
        reply=Serial_Con.read(1)
        if reply != '':
            for x in range(0, 7):
                if x == 5:
                    #print reply.encode("hex")
                    #print str(int(reply.encode("hex"),16))+"*C"
                    tempture=int(reply.encode("hex"),16)
                reply=Serial_Con.read(1)
            count=200
            #print("-----------")
            return tempture
        count+=1
        sleep(0.1)

def ReadVin(id):
    #print("Read Temp ID:"+str(id)+"-------------")
    AX_READ_DATA=3
    AX_TEMP_READ=27
    Serial_Con.flushInput()
    checksum = (~(id + AX_READ_DATA + AX_TEMP_READ))&0xff
    outData = chr(AX_START)
    #print(hex(ord(chr(AX_START))))
    outData += chr(AX_START)
    #print(hex(ord(chr(AX_START))))
    outData += chr(id)
    #print(hex(ord(chr(id))))
    outData += chr(AX_READ_DATA)
    #print(hex(ord(chr(AX_READ_DATA))))
    outData += chr(AX_TEMP_READ)
    #print(hex(ord(chr(AX_TEMP_READ))))
    outData += chr(checksum)
    #print(hex(ord(chr(checksum))))
    Serial_Con.write(outData)
    sleep(TX_DELAY_TIME)
    #print("Done -----------")
    count=0
    sleep(0.1)
    while count<200:
        reply=Serial_Con.read(1)
        if reply != '':
            for x in range(0, 7):
                #print reply.encode("hex"),
                #print str(int(reply.encode("hex"),16))+""
                if x == 5:
                    #print reply.encode("hex")
                    #print str(int(reply.encode("hex"),16))+"*C"
                    tempture=int(reply.encode("hex"),16)
                reply=Serial_Con.read(1)
            count=200
            #print("-----------")
            return tempture
        count+=1
        sleep(0.1)

def ReadPos(id):
    #print("Read Temp ID:"+str(id)+"-------------")
    AX_READ_DATA=3
    AX_TEMP_READ=28
    Serial_Con.flushInput()
    checksum = (~(id + AX_READ_DATA + AX_TEMP_READ))&0xff
    outData = chr(AX_START)
    #print(hex(ord(chr(AX_START))))
    outData += chr(AX_START)
    #print(hex(ord(chr(AX_START))))
    outData += chr(id)
    #print(hex(ord(chr(id))))
    outData += chr(AX_READ_DATA)
    #print(hex(ord(chr(AX_READ_DATA))))
    outData += chr(AX_TEMP_READ)
    #print(hex(ord(chr(AX_TEMP_READ))))
    outData += chr(checksum)
    #print(hex(ord(chr(checksum))))
    Serial_Con.write(outData)
    sleep(TX_DELAY_TIME)
    #print("Done -----------")
    count=0
    sleep(0.1)
    while count<200:
        reply=Serial_Con.read(1)
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
                reply=Serial_Con.read(1)
            count=200
            #print("-----------")
            return pos2
        count+=1
        sleep(0.1)

  "watcher": {
    "files": "dist/*.{js,css}",
    "autoUpload": false,
    "autoDelete": false,
  },