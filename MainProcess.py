# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import json

import cv2
import GetCardinalContours
import GetNeedleByThreshold


def initprocess(img_path, frame, mod_factor, size, meter_no):
    needle_x = needle_y = 0
    try:
        # TODO: get needle point and get base contours coordinates
        # if size == "meter48" or size == "meter144":
        #     iterate = 3
        # else:
        #     iterate = 3
        iterate = 3
        md = open(img_path + "\\MeterImages\\Crop\\" + str(meter_no) + "\\" + str(meter_no) + ".json")
        meter_details = json.load(md)
        meter_info = meter_details["meter" + str(meter_no)]
        print('Processing meter:', str(meter_no))
        base_x = float(meter_info["base_x"])
        base_y = float(meter_info["base_y"])
        top_x = float(meter_info["top_x"])
        top_y = float(meter_info["top_y"])
        cardinal_coordinate = meter_info["cardinal_coordinates"]
        min_dist = float(meter_info["min_dist"])
        for x, y in cardinal_coordinate:
            cv2.line(frame, (int(x), int(y)), (int(top_x), int(base_y)), (255, 0, 0), 1)
        cv2.line(frame, (int(base_x), int(base_y)), (int(top_x), int(base_y)), (0, 0, 255), 1)
        cv2.line(frame, (int(top_x), int(top_y)), (int(top_x), int(base_y)), (0, 0, 255), 1)

        tolerance = []

        # Todo : Start from here but load previous values
        try:
            print('First attempt to find needle')
            needle_x, needle_y = GetNeedleByThreshold.get_needle_tip(img_path, top_x, base_y, iterate, meter_no,
                                                                     min_dist)
            print('Needle position:', needle_x, needle_y)
        except Exception, e:
            try:
                print('Second attempt attempt to find needle')
                iterate -= 1
                needle_x, needle_y = GetNeedleByThreshold.get_needle_tip(img_path, top_x, base_y, iterate, meter_no,
                                                                         min_dist)
            except Exception, e:
                # try:
                print('Third attempt to find needle')
                iterate -= 1
                needle_x, needle_y = GetNeedleByThreshold.get_needle_tip(img_path, top_x, base_y, iterate, meter_no,
                                                                         min_dist)
                # except Exception, e:
                #     print('last attempt to find needle')
                #     iterate -= 1
                #     needle_x, needle_y = GetNeedleByThreshold.get_needle_tip(img_path, top_x, base_y, iterate, meter_no,
                #                                                              min_dist)
        try:
            pointer = ((needle_x, needle_y), (top_x, base_y))
            cardinal = ((base_x, base_y), (top_x, base_y))
            angle_list, cardinal_angle = GetCardinalContours.get_needle_angles(top_x, base_y, pointer, cardinal,
                                                                               cardinal_coordinate)
            len_angle = len(angle_list)
            count = 0
            while count < len_angle:
                tolerance.append(round((angle_list[count]) * mod_factor, ndigits=2))
                count += 1

            cv2.line(frame, (int(needle_x), int(needle_y)), (int(top_x), int(base_y)), (0, 255, 0), 1)
            cv2.circle(frame, (int(needle_x), int(needle_y)), 1, 255, -1)
            return frame, angle_list, tolerance
        except Exception, e:
            print "In start capture needle calculation", str(e)

    except Exception, e:
        print "In start capture", str(e)
