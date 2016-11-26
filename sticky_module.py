# Author:  <Rohit Salunke>
# Create date: <Create Date, 09-011-2016,>
# Description: <Description,Program to detect stickyness of analog meter,>
import json
import cv2
import GetNeedleByThreshold
import Find_Angle
import time


def sticky(meter, img_path, base_x, base_y, top_x, size):

        try:
            cv2.imwrite(img_path + "\\MeterImages\\temp.jpg", meter)
            if size == "meter48" or size == "meter72":
                iterate = 5
            else:
                iterate = 3
            needle_x, needle_y = GetNeedleByThreshold.get_needle_tip_for_sticky(img_path, top_x, base_y, iterate)
            pointer = ((needle_x, needle_y), (top_x, base_y))
            base_line = ((base_x, base_y), (top_x, base_y))
            ang = round(Find_Angle.ang(pointer, base_line), ndigits=2)

            cv2.putText(meter, "curr_ang: " + str(ang), (20, 20), cv2.QT_FONT_NORMAL, 0.5, (0, 0, 0), thickness=1,
                        lineType=cv2.CV_8U)
            cv2.line(meter, (int(needle_x), int(needle_y)), (int(top_x), int(base_y)), (0, 255, 0), 1)
            cv2.line(meter, (int(base_x), int(base_y)), (int(top_x), int(base_y)), (0, 255, 0), 1)
            cv2.imwrite(img_path+"\\MeterImages\\test_sticky\\"+str(time.time())+".jpg", meter)

            return ang
        except Exception, e:
            print "Sticky Error: in GetNeedleByThreshold.get_needle_tip_for_sticky " + str(e)
