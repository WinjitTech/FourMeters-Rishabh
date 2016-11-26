# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import json

import cv2
import math
import numpy as np
import GetCurrentNeedle
import GetCardinalContours
import GetBaseCardinals
import GetNeedleByThreshold


def initprocess(img_path, frame, mod_factor, size, suppression, cardinal_len, meter_no):
    try:
        meter_size = open(img_path + "\\Auto\\metersize.json", "r")
        # json_data = json.load(meter_size)
        # min_range = json_data[size]["min_range"]
        # max_range = json_data[size]["max_range"]
        # meter_size.close()
        # TODO: get needle point and get base contours coordinates
        if size == "meter48" or size == "meter72":
            iterate = 4
        else:
            iterate = 3
        md = open(img_path+"\\Auto\\MeterImages\\Crop\\"+str(meter_no)+"\\"+str(meter_no)+".json")
        meter_details = json.load(md)
        meter_info = meter_details["meter" + str(meter_no)]
        print("Processing meter",str(meter_no))
        base_x = float(meter_info["base_x"])
        base_y = float(meter_info["base_y"])
        top_x = float(meter_info["top_x"])
        top_y = float(meter_info["top_y"])
        cardinal_coordinate = meter_info["cardinal_coordinates"]

        for x, y in cardinal_coordinate:
            cv2.line(frame, (int(x), int(y)), (int(top_x), int(base_y)), (255, 0, 0), 1)
        cv2.line(frame, (int(base_x), int(base_y)), (int(top_x), int(base_y)), (0, 0, 255), 1)
        cv2.line(frame, (int(top_x), int(top_y)), (int(top_x), int(base_y)), (0, 0, 255), 1)

        tolerance = []

        # Todo : Start from here but load previous values
        needle_x, needle_y = GetNeedleByThreshold.get_needle_tip(img_path, top_x, base_y, iterate, meter_no)
        if not needle_x and not needle_y:
            needle_x, needle_y = GetNeedleByThreshold.get_needle_tip(img_path, top_x, base_y, iterate - 1, meter_no)
        # print(needle_x, needle_y)
        #
        try:
            pointer = ((needle_x, needle_y), (top_x, base_y))
            cardinal = ((base_x, base_y), (top_x, base_y))
            angle_list, cardinal_angle = GetCardinalContours.get_needle_angles(top_x, base_y, pointer, cardinal, cardinal_coordinate)
            # print len(angle_list),angle_list
            len_angle = len(angle_list)
            count = 0
            while count < len_angle:
                # tolerance.append(round((angle_list[count] * 60) / 54, ndigits=2))
                tolerance.append(round((angle_list[count]) * mod_factor, ndigits=2))
                count += 1

            cv2.line(frame, (int(needle_x), int(needle_y)), (int(top_x), int(base_y)), (0, 255, 0), 1)
            cv2.circle(frame, (int(needle_x), int(needle_y)), 1, 255, -1)
            print(meter_no, angle_list)
            return frame
                # , angle_list[0:cardinal_len], tolerance[0:cardinal_len]
        except Exception, e:
            print "In start caputre needle calcluation", str(e)

    except Exception, e:
        print "In start caputre", str(e)
