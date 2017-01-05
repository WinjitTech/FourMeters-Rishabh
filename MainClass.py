import glob
import os
import pymssql
import sys
import time

import serial

import pymsgbox

import cv2
import Capture_Image
import sticky_module

__author__ = 'RohitSalunke'


# Todo : Database connection
try:
    conn = pymssql.connect(server='WINJIT286\SA', user='sa', password='winjit@123', database='Rishabh', timeout=5)
    # conn = pymssql.connect(server='rohits-pc', user='sa', password='Winjit@123', database='Rishabh', timeout=10)
    # conn = pymssql.connect(host=r"RISHABH-PC\SQLEXPRESS", user="sa", password="sa@123", database="Rishabh_Test",
    #                        charset='utf8')
    cursor = conn.cursor()
    cursor.execute("truncate table AngleDeflectionReadings")
    conn.commit()
    print("Accessed Database")
except Exception as e:
    print("Database error")
    exit()

# Todo : set calmet

try:
    ser = serial.Serial('COM5', baudrate=4800, timeout=1)
    # img_path = "C:\\ProgramData\\Rishabh\\Auto"
    start = '\x02'
    end = '\x03'
    mod_factor_list = []
    if len(sys.argv) > 1:
        print(sys.argv)
        f = open("C:\\ProgramData\\Rishabh\\Fourmeters\\AutoTest.txt", "w")
        f.write(str(sys.argv))
        f.close()
        cardinal_len = no_of_cardinals = int(sys.argv[1])
        img_path = str(sys.argv[2])
        size = "meter" + str(sys.argv[3])
        suppression = str(sys.argv[4])
        fsd = float(sys.argv[5])

        working_principle = str(sys.argv[6]).lower()
        electrical_parameter = str(sys.argv[7]).lower()
        # Todo : Volt settings
        if "mv" in electrical_parameter:
            electrical_parameter = "Z0"
        if "vo" in electrical_parameter:
            if fsd <= 2:
                electrical_parameter = "Z1"
            if 2 < fsd <= 20:
                electrical_parameter = "Z2"
            if 20 < fsd <= 200:
                electrical_parameter = "Z3"
            if fsd > 200:
                electrical_parameter = "Z4"

        if "ma" in electrical_parameter:
            if fsd <= 1:
                electrical_parameter = "Z5"
            if 1 < fsd <= 10:
                electrical_parameter = "Z6"
            if 10 < fsd <= 100:
                electrical_parameter = "Z7"
        if "amp" in electrical_parameter:
            if fsd <= 1:
                electrical_parameter = "Z8"
            if fsd > 1:
                electrical_parameter = "Z9"

        # Todo :set frequency for calmet
        frequency = str(sys.argv[8]).lower()

        if "dc" in frequency:
            frequency = "F0"
        if "50" in frequency:
            frequency = "F1"
        if "60" in frequency:
            frequency = "F2"
        if "400" in frequency:
            frequency = "F3"
        if "fext" in frequency:
            frequency = "F4"

        # Todo: pickup exact suppression table from working_principle, Suppression and Div
        if working_principle == "movingcoil":
            for i in range(0, no_of_cardinals):
                mod_factor_list.append(float(1.11))
        else:
            tblname = suppression + "Suprression_" + str(no_of_cardinals) + "Div"
            sql_query = "SELECT * FROM " + tblname
            cursor.execute(sql_query)
            mod_factor_list = []
            for row in cursor:
                mod_factor_list.append(float(row[2]))
    # Todo: Manual call for 150 volt meter
    else:
        cardinal_len = no_of_cardinals = 5
        img_path = "C:\\ProgramData\\Rishabh\\Fourmeters"
        size = "meter96"
        suppression = "x1"
        fsd = float(300)
        electrical_parameter = "volts"
        frequency = "60"

        if "mv" in electrical_parameter:
            electrical_parameter = "Z0"
        if "vo" in electrical_parameter:
            if fsd <= 2:
                electrical_parameter = "Z1"
            if 2 < fsd <= 20:
                electrical_parameter = "Z2"
            if 20 < fsd <= 200:
                electrical_parameter = "Z3"
            if fsd > 200:
                electrical_parameter = "Z4"

        if "ma" in electrical_parameter:
            if fsd <= 1:
                electrical_parameter = "Z5"
            if 1 < fsd <= 10:
                electrical_parameter = "Z6"
            if 10 < fsd <= 100:
                electrical_parameter = "Z7"
        if "amp" in electrical_parameter:
            if fsd <= 1:
                electrical_parameter = "Z8"
            if fsd > 1:
                electrical_parameter = "Z9"
        if "dc" in frequency:
            frequency = "F0"
        if "50" in frequency:
            frequency = "F1"
        if "60" in frequency:
            frequency = "F2"
        if "400" in frequency:
            frequency = "F3"
        if "fext" in frequency:
            frequency = "F4"
        # working_principle = "movingcoil"
        for i in range(0, no_of_cardinals):
            mod_factor_list.append(float(1.11))
    current_voltage = fsd
    next_voltage = fsd / no_of_cardinals
    arr_cardinals = [str(fsd)]
    for i in range(0, no_of_cardinals):
        current_voltage -= next_voltage
        arr_cardinals.append(str(current_voltage))
    del arr_cardinals[-1]
    current_voltage = fsd
    if no_of_cardinals == 4:
        rate = 80
    else:
        rate = 90
    step = (fsd / rate)
    mod_factor = mod_factor_list[no_of_cardinals - 1]
    s = '\x02Z0,F1,N00.00000,O\x03'
    # ser.write(s)
    time.sleep(0.1)
    ser.write(start + str(electrical_parameter) + "," + str(frequency) + end)
    time.sleep(0.5)
    ser.write("\x02O\x03")
    time.sleep(0.3)
    ser.write('\x02K\x03')
    time.sleep(0.1)
except Exception, e:
    print("Error in setting calmet", str(e))

# Todo : open camera
try:

    ser.write("\x02O\x03")
    time.sleep(0.3)
    ser.write('\x02K\x03')
    time.sleep(0.1)
    needle_angle_list = []
    current_voltage += step * 2
    meter_list = []
    cap = cv2.VideoCapture(0)
    cap.set(3, 2592)
    cap.set(4, 2048)

    # Todo: start updown cycle
    # i = 1
    while current_voltage > 0:
        current_voltage -= step
        time.sleep(0.04)
        ser.write('\x02N' + str(current_voltage) + '\x03')
        time.sleep(0.04)
        if str(current_voltage) in arr_cardinals:
            print "Current_Voltage", current_voltage, "Cardinal No.", no_of_cardinals
            # del meter_list[-2]
            time.sleep(1)
            # Todo: card angle and needle angle
            for f in range(0, 5):
                ret, frame = cap.read()
            resized_image = cv2.resize(frame, (1024, 900))
            img_name = str(no_of_cardinals) + "UptoDown"
            # Todo : Accuracy Call
            Capture_Image.start_capture(frame, no_of_cardinals, img_name, img_path, mod_factor, size, suppression,
                                        cardinal_len, cursor, updown=1)
            no_of_cardinals -= 1
            for f in range(0, 5):
                ret, frame = cap.read()
        # for i in range(0, 3):
        _, meter = cap.read()
        _, meter = cap.read()
        _, meter = cap.read()
        meter_list.append(meter)
        # cv2.imwrite(img_path+"\\MeterImages\\Crop\\raw_1\\"+str(i)+".jpg", meter)
        # i += 1
    d = discard = int(rate / cardinal_len)
    print("initial meters", len(meter_list))

    for i in range(1, cardinal_len):
        meter_list.pop(d)
        meter_list.pop(d + 1)
        discard -= 1
        d += discard
    # meter_list.pop(0)
    meter_list.pop(0)
    meter_list.pop(0)
    print("last pop meters", len(meter_list))
    time.sleep(0.1)
    ser.write('\x02K\x03')
    time.sleep(0.1)
    ser.write(start)
    ser.write('N' + str(0))
    ser.write(end)
    time.sleep(1)
    ser.write('\x02K\x03')
    time.sleep(0.1)
    # Todo:    Down to up
    current_voltage = 0
    no_of_cardinals = 1

    # Todo: start downup cycle
    while current_voltage <= fsd:
        current_voltage += step
        time.sleep(0.04)
        ser.write('\x02N' + str(current_voltage) + '\x03')
        time.sleep(0.04)
        # _, meter = cap.read()
        # _, meter = cap.read()
        # _, meter = cap.read()
        # meter_list.append(meter)
        if str(current_voltage) in arr_cardinals:
            print "Current_Voltage", current_voltage, "Cardinal No.", no_of_cardinals
            time.sleep(1)
            # Todo: card angle and needle angle
            for f in range(0, 5):
                ret, frame = cap.read()
            resized_image = cv2.resize(frame, (1024, 900))
            img_name = str(no_of_cardinals) + "DowntoUp"
            # Todo : Accuracy Call
            Capture_Image.start_capture(frame, no_of_cardinals, img_name, img_path, mod_factor, size, suppression,
                                        cardinal_len, cursor, updown=0)
            no_of_cardinals += 1

    time.sleep(0.1)
    ser.write('\x02K\x03')
    time.sleep(0.1)
    ser.write('\x02N0.0000\x03')
    time.sleep(0.1)
    # Todo: calculate sticky
    # updown = 1
    for i in range(1, 4):
        test = img_path + "\\MeterImages\\Crop\\raw\\" + str(i) + "\\*"
        r = glob.glob(test)
        for j in r:
            os.remove(j)

    for i in range(1, 4):
        test = img_path + "\\MeterImages\\Crop\\sticky\\" + str(i) + "\\*"
        r = glob.glob(test)
        for j in r:
            os.remove(j)
    sticky_module.sticky(img_path, meter_list, size)
    conn.commit()
    conn.close()
except Exception, e:
    print("In MainClass", str(e))
    if "OutOfMemoryError" in str(e):
        pymsgbox.alert('Insufficient memory to cater images ! \n         Program has terminated', 'Memory Exception')
    conn.commit()
    conn.close()

finally:
    ser.write('\x02K\x03')
    time.sleep(0.1)
