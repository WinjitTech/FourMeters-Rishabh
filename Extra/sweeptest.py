# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>
# Author :  Rohit Salunke
# Title:    Example of serial communication with python

import time

import serial

ser = serial.Serial('COM5', baudrate=4800, timeout=1)
# ser._write_timeout = 0.15
ser.dsrdtr = True
try:
    fsd = float(1)
    ser.write('\x02K\x03')
    time.sleep(1)
    ser.write('\x02Z9,F1,N1.00000,O\x03')
    time.sleep(2)
    current_voltage = fsd
    step = float(fsd / 120)
    # step = 1

    # Todo: top cardinal and initial image for sticky here
    current_voltage += step
    while current_voltage > 0:
        current_voltage -= step
        time.sleep(0.04)
        ser.write('\x02N' + str(current_voltage) + '\x03')
        time.sleep(0.04)
        # print(ser._checkReadable(),ser.reset_output_buffer())

        # ser.write('\x02K\x03')
        # time.sleep(0.06)
except Exception, e:
    print "Error in setting calmet, resetting camlet", str(e)
    ser.write('\x02K\x03')
    time.sleep(0.5)
    s = '\x02Z0,F0,N00.00000,O\x03'

finally:
    ser.write('\x02K\x03')
    time.sleep(0.5)
    s = '\x02Z0,F0,N00.00000,O\x03'
    # ser.write(s)
    # time.sleep(0.03)
