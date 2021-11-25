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

GPIO.setmode(GPIO.BCM) # Use chip numbering scheme
add = 0

f = open("27C512_image.bin", 'a')

# CE, WE, OE pins (pull down to activate each mode):
GPIO.setup (2, GPIO.OUT) #, pull_up_down = GPIO.PUD_UP) #CE
GPIO.setup (3, GPIO.OUT) #, pull_up_down = GPIO.PUD_UP) #OE
GPIO.setup (4, GPIO.OUT) #, pull_up_down = GPIO.PUD_UP) #WE


# Set the chip in standby mode:
GPIO.output(2,1) #CE - high
GPIO.output(3,1) #OE - high

# Address pins set for output (A15, A16, A17 connected to ground):
GPIO.setup (10, GPIO.OUT) #,  #A0
GPIO.setup (9,  GPIO.OUT) #,  #A1
GPIO.setup (11, GPIO.OUT) #,  #A2
GPIO.setup (25, GPIO.OUT) #,  #A3
GPIO.setup (8,  GPIO.OUT) #,  #A4
GPIO.setup (7,  GPIO.OUT) #,  #A5
GPIO.setup (5,  GPIO.OUT) #,  #A6
GPIO.setup (6,  GPIO.OUT) #,  #A7
GPIO.setup (12, GPIO.OUT) #,  #A8
GPIO.setup (13, GPIO.OUT) #,  #A9
GPIO.setup (19, GPIO.OUT) #,  #A10
GPIO.setup (26, GPIO.OUT) #,  #A11
GPIO.setup (16, GPIO.OUT) #,  #A12
GPIO.setup (20, GPIO.OUT) #,  #A13
GPIO.setup (21, GPIO.OUT) #,  #A14
GPIO.setup (4,  GPIO.OUT) #,  #A15

GPIO.output (10, 0) #,  #A0
GPIO.output (9,  0) #,  #A1
GPIO.output (11, 0) #,  #A2
GPIO.output (25, 0) #,  #A3
GPIO.output (8,  0) #,  #A4
GPIO.output (7,  0) #,  #A5
GPIO.output (5,  0) #,  #A6
GPIO.output (6,  0) #,  #A7
GPIO.output (12, 0) #,  #A8
GPIO.output (13, 0) #,  #A9
GPIO.output (19, 0) #,  #A10
GPIO.output (26, 0) #,  #A11
GPIO.output (16, 0) #,  #A12
GPIO.output (20, 0) #,  #A13
GPIO.output (21, 0) #,  #A14
GPIO.output (4,  0) #,  #A15


# Data pins set for input (pull down for zeroes):
GPIO.setup (14, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #D0
GPIO.setup (15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #D1
GPIO.setup (18, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #D2
GPIO.setup (17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #D3
GPIO.setup (27, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #D4
GPIO.setup (22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #D5
GPIO.setup (23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #D6
GPIO.setup (24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #D7


try:

    while (add < 65536):
        A = []

        A = add
        A = (bin(A)[2:]).zfill(16)
        A = map(int, A)

        # Set address bus:
        GPIO.output(10,A[15])    #A0
        GPIO.output(9, A[14])    #A1
        GPIO.output(11,A[13])    #A2
        GPIO.output(25,A[12])    #A3
        GPIO.output(8, A[11])    #A4
        GPIO.output(7, A[10])    #A5
        GPIO.output(5,  A[9])    #A6
        GPIO.output(6,  A[8])    #A7
        GPIO.output(12, A[7])    #A8
        GPIO.output(13, A[6])    #A9
        GPIO.output(19, A[5])    #A10
        GPIO.output(26, A[4])    #A11
        GPIO.output(16, A[3])    #A12
        GPIO.output(20, A[2])    #A13
        GPIO.output(21, A[1])    #A14
        GPIO.output(4,  A[0])    #A15


#       print "Turning on the chip and setting it to output mode."
        GPIO.output(3,0)  # OE - low - enable output
        GPIO.output(2,0)  # CE - low - turn on the chip
        time.sleep(0.001) # pause 1ms
        
#       print "Reading the address."
        # set data variables
        D7= GPIO.input(14)
        D6= GPIO.input(15)
        D5= GPIO.input(18)
        D4= GPIO.input(17)
        D3= GPIO.input(27)
        D2= GPIO.input(22)
        D1= GPIO.input(23)
        D0= GPIO.input(24)


# write output 
        outP = "{0:0>2X}".format(int(str(D0)+str(D1)+str(D2)+str(D3)+str(D4)+str(D5)+str(D6)+str(D7), 2))
        print (add , outP , )

        c = binascii.unhexlify(outP)

        print (c)
        f.write(c) 
        add = add + 1
        GPIO.output(2,1)  # CE - high - standby mode
        GPIO.output(3,1)  # OE - high - disable outputA
        time.sleep(0.001) # pause 1ms

except KeyboardInterrupt:
    print ("Keyboard Interrupt.\nPerforming GPIO cleanup.")
    GPIO.cleanup()

GPIO.output(2,1) # CE - high - standby mode
GPIO.output(3,1) # OE - high - disable output
GPIO.cleanup()
f.close()
