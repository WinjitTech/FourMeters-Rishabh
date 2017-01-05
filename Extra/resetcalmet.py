# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import time

import serial

ser = serial.Serial('COM1', baudrate=4800, timeout=1)
ser.write('\x02K\x03')
time.sleep(0.5)
s = '\x02Z0,F0,N00.00000,O\x03'
ser.write(s)
