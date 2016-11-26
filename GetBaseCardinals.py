# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import cv2
import numpy as np


def zero_needle_position(img_path, iteration, meter_no):
    try:
        # Todo: Read Image
        image = cv2.imread(img_path+"\\Auto\\MeterImages\\Crop\\"+str(meter_no)+"\\"+str(meter_no)+".jpg", 0)
        print(img_path+"\\Auto\\MeterImages\\Crop\\"+str(meter_no)+"\\"+str(meter_no)+".jpg")
        # TODO: Find corner of needle
        color = int(image[300, 300])
        # print color
        cv2.rectangle(image, (0, 0), (150, 1000), (color, color, color), -1)
        cv2.rectangle(image, (400, 0), (1000, 1000), (color, color, color), -1)
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(image, kernel, iterations=iteration)
        corners = cv2.goodFeaturesToTrack(dilation, 2, 0.1, 10)
        cx = cy = 0
        for i in corners:
            x, y = i.ravel()
            cv2.circle(dilation, (x, y), 2, (0, 255, 0), -1)
            cx += x
            cy += y
        cx /= len(corners)
        cy /= len(corners)
        # cv2.imshow("Iiitail", dilation)
        # cv2.waitKey(0)
        return int(round(cx)), int(round(cy))

    except Exception, e:
        print "Exception in Base Needle Detection Dilute Image:", str(e)


