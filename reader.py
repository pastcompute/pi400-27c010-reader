# 
# Based on python code & wiring originally from 
#    http://www.myers-net.com/eprom/index.html
# 
# modded by @zedstarr 2021-02-22
# 
# reading 27C512 5V CMOS EPROM
# directly via PI's 3V3 GPIO
# 
# see https://bit.ly/27C512dump
# 
# this code (slowly) writes a binary image of the ROM data to file
# 
# use hexdump to view, e.g.
# 
# hexdump -vC 27C512_image.bin
# 
# DISCLAIMER: I am not a software engineer, this is horrible code
#             But it works! Please feel free to re-write!
# 


import RPi.GPIO as GPIO
import time, re
import binascii

GPIO.cleanup()
GPIO.setmode(GPIO.BCM) # Use chip numbering scheme

f = open("imagepd5.bin", 'wb')

CE=2 # 25
OE=3 # 7
ADDR_LINES = ( 17, 27, 22, 10, 9, 11, 5, 6, 18, 23, 8, 24, 13, 15, 14, 19, 26 )
DATA_LINES=( 4, 7, 25, 21, 20, 16, 12, 1 )

# CE, WE, OE pins (pull down to activate each mode):
GPIO.setup (CE, GPIO.OUT) #, pull_up_down = GPIO.PUD_UP) #CE
GPIO.setup (OE, GPIO.OUT) #, pull_up_down = GPIO.PUD_UP) #OE

# Set the chip in standby mode:
GPIO.output(CE, 1) #CE - high
GPIO.output(OE, 1) #OE - high
time.sleep(1)
GPIO.output(CE, 0)
time.sleep(1)
GPIO.output(CE, 1)
time.sleep(1)
GPIO.output(CE, 0)
time.sleep(1)
GPIO.output(CE, 1)

[ GPIO.setup(a, GPIO.OUT) for a in ADDR_LINES]
[ GPIO.output(a, 0) for a in ADDR_LINES]

[ GPIO.setup(d, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) for d in DATA_LINES] #  pull_up_down = GPIO.PUD_UP

NA = len(ADDR_LINES)
ND = len(DATA_LINES)

try:
    addr = 0
    while (addr < 131072):
        D = [0, 0, 0, 0, 0, 0, 0, 0]
        A = []

        #A1 = addr
        #A = (bin(A1)[2:]).zfill(16) # String?!
        #A2 = map(int, A)
        #print(A)

        # Set address bus:
        ab = addr
        for b in range(NA):
            abit = ab & 0x1
            ab = ab >> 1
            #print(ADDR_LINES[b], b, n, abit)
            GPIO.output(ADDR_LINES[b], abit)
            # We can output to 17 @ once by passing a tuple as the first arg as well
            # But then we need to make a new tuple/list from abit

        #sys.exit(1)

#       print "Turning on the chip and setting it to output mode."
        GPIO.output(CE, 0)  # OE - low - enable output
        time.sleep(0.001) # pause 1ms
        GPIO.output(OE, 0)  # CE - low - turn on the chip
        time.sleep(0.001) # pause 1ms
        
#       print "Reading the address."
        for b in range(ND):
            D[b] = GPIO.input(DATA_LINES[b])
        GPIO.output(OE,1)  # CE - high - standby mode
        GPIO.output(CE,1)  # OE - high - disable outputA
        # No need for a pause, the following I/O is sufficient

# write output 
        outP = "{0:0>2X}".format(int(str(D[7])+str(D[6])+str(D[5])+str(D[4])+str(D[3])+str(D[2])+str(D[1])+str(D[0]), 2))
        c = binascii.unhexlify(outP)
        if addr == 0:
            print ('Sample @ 0x0: ', addr , outP , c)
        if addr % 1024 == 0:
            print(addr)
        f.write(c) 
        addr = addr + 1

except KeyboardInterrupt:
    print ("Keyboard Interrupt.\nPerforming GPIO cleanup.")
    GPIO.cleanup()

GPIO.output(CE,1) # CE - high - standby mode
GPIO.output(OE,1) # OE - high - disable output
GPIO.cleanup()
f.close()
