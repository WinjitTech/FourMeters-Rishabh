# Author:  <Rohit Salunke>
# Create date: <Create Date, 09-011-2016,>
# Description: <Description,Program to detect stickyness of analog meter,>
import json

import cv2
import GetNeedleByThreshold
import Find_Angle


def sticky(img_path, meter_list):
    frames_json = open(img_path + "\\MeterImages\\Crop\\frame.json")
    data = json.load(frames_json)
    frames_json.close()
    iterate = 3
    meter1_ang_list = []
    meter2_ang_list = []
    meter3_ang_list = []
    meter4_ang_list = []
    i = int(1)
    try:
        for meter in meter_list:
            for meter_no in data:
                meter_crop = json.loads(data[meter_no])
                x1 = meter_crop.get("x1")
                x2 = meter_crop.get("x2")
                y1 = meter_crop.get("y1")
                y2 = meter_crop.get("y2")
                cropped_meter = meter[y1:y2, x1:x2]
                # cv2.imshow(str(meter_no), meter)
                # cv2.waitKey(0)
                cv2.imwrite(img_path + "\\MeterImages\\Crop\\raw\\" + str(meter_no) + "\\" + str(i) + ".jpg",
                            cropped_meter)
                try:
                    md = open(img_path + "\\MeterImages\\Crop\\" + str(meter_no) + "\\" + str(meter_no) + ".json")
                    meter_details = json.load(md)
                    meter_info = meter_details["meter" + str(meter_no)]
                    # print("Processing meter", str(meter_no))
                    base_x = float(meter_info["base_x"])
                    base_y = float(meter_info["base_y"])
                    top_x = float(meter_info["top_x"])
                    top_y = float(meter_info["top_y"])

                    needle_x, needle_y = GetNeedleByThreshold.get_needle_tip_for_sticky(img_path, top_x, base_y,
                                                                                        iterate, meter_no, i)
                    if not needle_x and not needle_y:
                        needle_x, needle_y = GetNeedleByThreshold.get_needle_tip_for_sticky(img_path, top_x, base_y,
                                                                                            meter_no, iterate - 1, i)

                    pointer = ((needle_x, needle_y), (top_x, base_y))
                    base_line = ((base_x, base_y), (top_x, base_y))
                    ang = round(Find_Angle.ang(pointer, base_line), ndigits=2)

                    cv2.putText(cropped_meter, "curr_ang: " + str(ang), (20, 20), cv2.QT_FONT_NORMAL, 0.5, (0, 0, 0),
                                thickness=1,
                                lineType=cv2.CV_8U)
                    cv2.line(cropped_meter, (int(needle_x), int(needle_y)), (int(top_x), int(base_y)), (0, 255, 0), 1)
                    cv2.line(cropped_meter, (int(base_x), int(base_y)), (int(top_x), int(base_y)), (0, 255, 0), 1)
                    cv2.imwrite(img_path + "\\MeterImages\\Crop\\sticky\\" + str(meter_no) + "\\" + str(i) + ".jpg",
                                cropped_meter)
                    if str(meter_no) == str(1):
                        meter1_ang_list.append(ang)
                    if str(meter_no) == str(2):
                        meter2_ang_list.append(ang)
                    if str(meter_no) == str(3):
                        meter3_ang_list.append(ang)
                    if str(meter_no) == str(4):
                        meter4_ang_list.append(ang)
                except Exception, e:
                    print("from initprocess", str(e))
            i += 1

        print(meter1_ang_list, meter2_ang_list)
    except Exception, e:
        print("In sticky module: ", str(e))

        # sticky = open("C:\\ProgramData\\Rishabh\\sticky.txt", "w")
        #
        #    # print needle_angle_list
        #    if len(needle_angle_list) == len(set(needle_angle_list)) and needle_angle_list == sorted(needle_angle_list, reverse=True):
        #        print "Meter is Not sticky"
        #        sticky.write("false")
        #    else:
        #        print "Meter is Sticky"
        #        sticky.write("true")
        #    sticky.close()
