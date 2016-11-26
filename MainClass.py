import json
import serial
import sys
import time
import cv2
import Capture_Image

__author__ = 'RohitSalunke'

import pymssql

config = open("C:\\ProgramData\\Rishabh\\Auto\\rishabh.config", "r")
json_data = json.load(config)
img_path = json_data["img_path"]
config.close()
# Todo : Database connection
try:
    conn = pymssql.connect(server='winjit214', user='sa', password='winjit@123', database='Rishabh', timeout=10)
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
    ser = serial.Serial('COM3', baudrate=4800, timeout=1)
    no_of_cardinals = 5
    # img_path = "C:\\ProgramData\\Rishabh\\Auto"
    start = '\x02'
    end = '\x03'
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
        cardinal_len = no_of_cardinals = 4
        # img_path = "C:\\Users\\rohitsalunke\\PycharmProjects\\RishabhWebCam\\Auto Program"
        size = "meter96"
        suppression = "x1"
        fsd = float(60)
        electrical_parameter = "volts"
        if "vo" in electrical_parameter:
            electrical_parameter = "Z4"
        if "amp" in electrical_parameter:
            electrical_parameter = "Z9"
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
    print(arr_cardinals)
    current_voltage = fsd
    rate = 120
    step = (fsd / rate)
    mod_factor = mod_factor_list[no_of_cardinals - 1]
    time.sleep(0.1)
    s = '\x02Z0,F1,N00.00000,O\x03'
    ser.write(s)
    time.sleep(0.1)
    ser.write(start + str(electrical_parameter) + end)
    time.sleep(1)
    ser.write('\x02K\x03')
    time.sleep(0.1)
except Exception, e:
    print("Error in setting calmet", str(e))

# Todo : open camera
try:
    needle_angle_list = []
    current_voltage += step * 3
    meter_list = []
    cap = cv2.VideoCapture(0)
    cap.set(3, 2592)
    cap.set(4, 2048)
    while current_voltage > 0:
        current_voltage -= step
        time.sleep(0.1)
        ser.write(start)
        ser.write('N' + str(round(current_voltage, ndigits=5)))
        ser.write(end)
        # ret, frame = cap.read()
        # cap.set(3, 2592)
        # cap.set(4, 2048)
        # meter_list.append(frame)
        if str(current_voltage) in arr_cardinals:
            print "Current_Voltage", current_voltage, "Cardinal No.", no_of_cardinals
            time.sleep(0.5)
            # Todo: card angle and needle angle
            # for f in range(0, 3):
            ret, frame = cap.read()
            cap.set(3, 2592)
            cap.set(4, 2048)
            resized_image = cv2.resize(frame, (1024, 900))
            img_name = str(no_of_cardinals) + "UptoDown.jpg"
            # Todo : Accuracy Call
            # angle, deflection, top_x, base_y, base_x, base_y = Capture_Image.start_capture(frame, no_of_cardinals,
            #                                                                                img_name, img_path,
            #                                                                                mod_factor, size, suppression
            #                                                                                , cardinal_len)
            Capture_Image.start_capture(frame, no_of_cardinals, img_name, img_path, mod_factor, size, suppression,
                                        cardinal_len)
            # sql_query = "insert into AngleDeflectionReadings (MeterNo, CardinalNo, Angle, Deflection,UpDown) values(" + str(
            #     '1') + "," + str(no_of_cardinals) + "," + str(angle) + "," + str(deflection) + "," + str(
            #     '1') + ");"
            # cursor.execute(sql_query)
            no_of_cardinals -= 1

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

    conn.commit()
    conn.close()
except Exception, e:
    print(str(e))

finally:
    s = '\x02Z0,F0,N00.00000,S\x03'
    ser.write(s)
# Todo : start sticky
