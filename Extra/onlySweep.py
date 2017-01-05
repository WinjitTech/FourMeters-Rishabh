__author__ = 'RohitSalunke'

import time

import serial

ser = serial.Serial('COM4', baudrate=4800, timeout=1)
ser.write('\x02K\x03')
time.sleep(0.05)
fsd = float(150)
ser.write('\x02Z4,F1,N00.00000,O\x03')
time.sleep(2)
ser.write('\x02N150.00000\x03')
time.sleep(0.05)

currentReading = fsd * 1.05
time.sleep(1)
step = fsd / 120
# currentRe
while currentReading > 0:
    currentReading -= step
    ser.write('\x02N' + str(currentReading) + '\x03')
    time.sleep(0.05)
    ser.write('\x02K\x03')
    time.sleep(0.05)
    if currentReading < 0.6:
        currentReading = fsd * 1.05
