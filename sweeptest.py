# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>
# Author :  Rohit Salunke
# Title:    Example of serial communication with python

import serial
import time


ser = serial.Serial('COM3', baudrate=4800, timeout=1)
# for i in range(0, 10):
try:
        no_of_cardinals = 5
        img_path = "F:\\Sweeptest\\RishabhWebCam\\Auto Program"
        # mod_factor = 1.11
        size = "meter96"
        suppression = "x1"
        fsd = float(60)
        # ser = serial.Serial('COM1', timeout=1)
        start = '\x02'
        end = '\x03'
        time.sleep(0.03)
        ser.write('\x02K\x03')
        time.sleep(0.03)
        s = '\x02Z4,F1,N00.00000,O\x03'
        time.sleep(0.3)
        ser.write(s)
        time.sleep(0.3)
        current_voltage = fsd
        next_voltage = fsd / no_of_cardinals
        arr_cardinals = [str(fsd)]
        for i in range(0, no_of_cardinals):
            current_voltage -= next_voltage
            arr_cardinals.append(str(current_voltage))
        del arr_cardinals[-1]
        print(arr_cardinals)
        current_voltage = fsd
        rate = 120
        step = (fsd / rate)
        start_time = time.time()
        if current_voltage == fsd:
            ser.write(s)
            time.sleep(0.06)
            ser.write('\x02K\x03')
            time.sleep(0.06)
            ser.write(start)
            ser.write('N' + str(fsd))
            ser.write(end)
            time.sleep(3)
            # Todo: top cardinal and initial image for sticky here

        # current_voltage -= step
        while current_voltage > 0:
            time.sleep(0.11)
            # ser.write('\x02K\x03')
            # time.sleep(0.06)
            ser.write(start)
            ser.write('N' + str(round(current_voltage, ndigits=5)))
            ser.write(end)
            if str(current_voltage) in arr_cardinals:
                # time.sleep(0.1)
                # ser.write('\x02K\x03')
                # time.sleep(0.1)
                # ser.write(start)
                # ser.write('N' + str(round(current_voltage, ndigits=5)))
                # ser.write(end)
                # time.sleep(0.1)
                # ser.write('\x02K\x03')
                # time.sleep(0.1)
                print "Current_Voltage", current_voltage, "Cardinal No.", no_of_cardinals
                no_of_cardinals -= 1
                time.sleep(1)
            current_voltage -= step

        time.sleep(0.1)
        ser.write('\x02K\x03')
        time.sleep(0.1)
        ser.write(start)
        ser.write('N' + str(0))
        ser.write(end)

        s = '\x02Z0,F0,N00.00000,S\x03'
        ser.write(s)
except Exception, e:
        print "Error in setting calmet, resetting camlet", str(e)
        ser.write('\x02K\x03')
        time.sleep(0.5)
        s = '\x02Z0,F0,N00.00000,O\x03'
        ser.write(s)