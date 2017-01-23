# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>
# Author :  Rohit Salunke
# Title:    Example of serial communication with python
import glob
import json
import os
import time
import pymssql
import sys

import serial

import sticky_module
import cv2
import Capture_Image


def auto_tune_new():
    try:
        conn = pymssql.connect(server='winjit214', user='sa', password='winjit@123', database='Rishabh', timeout=10)
        # conn = pymssql.connect(server='rohits-pc', user='sa', password='Winjit@123', database='Rishabh', timeout=10)
        # conn = pymssql.connect(host=r"RISHABH-PC\SQLEXPRESS", user="sa", password="sa@123", database="Rishabh_Test",
        #                        charset='utf8')
        cursor = conn.cursor()
        print("Accessed Database")
    except Exception as e:
        print("Database error")
        exit()
    try:

        ser = serial.Serial('COM1', baudrate=4800, timeout=1)
        no_of_cardinals = 5
        img_path = "C:\\ProgramData\\Rishabh\\Auto"
        start = '\x02'
        end = '\x03'
        # start_time = time.time()
        file_list = glob.glob(img_path + "\\MeterImages\\test_sticky\\*.jpg")
        for f in file_list:
            os.remove(f)
        # Todo Initail settings
        try:
            config = open("C:\\ProgramData\\Rishabh\\Auto\\frame.json", "r")
            # print (img_path+"\\frame.json", "r")
            data = json.load(config)
            x1 = data["x1"]
            x2 = data["x2"]
            y1 = data["y1"]
            y2 = data["y2"]
            config.close()
            mod_factor_list = []
            if len(sys.argv) > 1:
                f = open("C:\\ProgramData\\Rishabh\\Auto\\AutoTest.txt", "w")
                f.write(str(sys.argv))
                f.close()
                cardinal_len = no_of_cardinals = int(sys.argv[1])
                img_path = str(sys.argv[2])
                size = "meter" + str(sys.argv[3])
                suppression = str(sys.argv[4])
                fsd = float(sys.argv[5])
                working_principle = str(sys.argv[6]).lower().lower()
                electrical_parameter = str(sys.argv[7].lower().lower())
                print electrical_parameter
                if "vol" in electrical_parameter:
                    electrical_parameter = "Z4"
                if "amp" in electrical_parameter:
                    electrical_parameter = "Z9"

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
            else:
                # Todo: Manual call for 150 volt meter
                cardinal_len = no_of_cardinals = 5
                # img_path = "C:\\Users\\rohitsalunke\\PycharmProjects\\RishabhWebCam\\Auto Program"
                img_path = "C:\\Users\\rohitsalunke\\PycharmProjects\\RishabhWebCam\\Auto Program"
                # mod_factor = 1.11
                size = "meter96"
                suppression = "x1"
                fsd = float(5)
                electrical_parameter = "volts"
                if "vo" in electrical_parameter:
                    electrical_parameter = "Z4"
                if "amp" in electrical_parameter:
                    electrical_parameter = "Z9"
                # working_principle = "movingcoil"
                for i in range(0, no_of_cardinals):
                    mod_factor_list.append(float(1.11))
        except Exception, e:
            print("In Initail settings", str(e))
        # Todo: start here
        cursor.execute("truncate table AngleDeflectionReadings")
        conn.commit()
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
        # img_name = str(no_of_cardinals) + "UptoDown.jpg"
        mod_factor = mod_factor_list[no_of_cardinals - 1]
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        meter_list = []
        if not ret:
            print ("Check if Camera is Available")
            cap.release()
            cv2.destroyAllWindows()
        # Todo initial setup for calmet
        time.sleep(0.1)
        s = '\x02Z0,F1,N00.00000,O\x03'
        ser.write(s)
        time.sleep(0.1)
        # ser.write(start)
        ser.write(start+str(electrical_parameter)+end)
        # ser.write(end)
        time.sleep(1)
        ser.write('\x02K\x03')
        time.sleep(0.1)
        needle_angle_list = []
        current_voltage += step * 3
        while current_voltage > 0:
            current_voltage -= step
            time.sleep(0.1)
            ser.write(start)
            ser.write('N' + str(round(current_voltage, ndigits=5)))
            ser.write(end)
            ret, frame = cap.read()
            meter_list.append(frame[y1:y2, x1:x2])
            if str(current_voltage) in arr_cardinals:
                print "Current_Voltage", current_voltage, "Cardinal No.", no_of_cardinals
                time.sleep(3)
                # Todo: card angle and needle angle
                for f in range(0, 5):
                    ret, frame = cap.read()
                meter = frame[y1:y2, x1:x2]
                img_name = str(no_of_cardinals) + "UptoDown.jpg"
                angle, deflection, top_x, base_y, base_x, base_y = Capture_Image.start_capture(meter, no_of_cardinals,
                                                                                               img_name, img_path,
                                                                                               mod_factor, size,
                                                                                               suppression,
                                                                                               cardinal_len)
                sql_query = "insert into AngleDeflectionReadings (MeterNo, CardinalNo, Angle, Deflection,UpDown) values(" + str(
                    '1') + "," + str(no_of_cardinals) + "," + str(angle) + "," + str(deflection) + "," + str(
                    '1') + ");"
                cursor.execute(sql_query)
                no_of_cardinals -= 1
        #print current_voltage
        
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

        while current_voltage < fsd * 1.01:
            current_voltage += step
            time.sleep(0.1)
            ser.write(start)
            ser.write('N' + str(round(current_voltage, ndigits=5)))
            ser.write(end)
            if str(current_voltage) in arr_cardinals:

                print "Current_Voltage", current_voltage, "Cardinal No.", no_of_cardinals
                time.sleep(1.5)
                # Todo: card angle and needle angle
                for f in range(0, 4):
                    ret, frame = cap.read()
                meter = frame[y1:y2, x1:x2]
                img_name = str(no_of_cardinals) + "DowntoUp.jpg"
                angle, deflection, top_x, base_y, base_x, base_y = Capture_Image.start_capture(meter, no_of_cardinals,
                                                                                               img_name, img_path,
                                                                                               mod_factor, size,
                                                                                               suppression,
                                                                                               cardinal_len)
                sql_query = "insert into AngleDeflectionReadings (MeterNo, CardinalNo, Angle, Deflection,UpDown) values(" + str(
                    '1') + "," + str(no_of_cardinals) + "," + str(angle) + "," + str(deflection) + "," + str(
                    '0') + ");"
                cursor.execute(sql_query)
                # print angle
                no_of_cardinals += 1
            if current_voltage > fsd:
                break

        ser.write('\x02K\x03')
        time.sleep(0.5)
        s = '\x02Z0,F0,N00.00000,O\x03'
        ser.write(s)
        i = 0
        for img in meter_list:
            # cv2.imwrite(img_path + "\\MeterImages\\sample\\"+i+".jpg", meter)
            needle_angle_list.append(str(sticky_module.sticky(img, img_path, base_x, base_y, top_x, size)))
            i +=1
        sticky = open("C:\\ProgramData\\Rishabh\\sticky.txt", "w")
        # print needle_angle_list
        if len(needle_angle_list) == len(set(needle_angle_list)) and needle_angle_list == sorted(needle_angle_list, reverse=True):
            print "Meter is Not sticky"
            sticky.write("false")
        else:
            print "Meter is Sticky"
            sticky.write("true")
        sticky.close()
        conn.commit()
        conn.close()
    except Exception, e:
        print "Error in setting calmet, resetting camlet", str(e)
        ser.write('\x02K\x03')
        time.sleep(0.5)
        s = '\x02Z0,F0,N00.00000,O\x03'
        ser.write(s)


# for i in range(0, 3):
auto_tune_new()
