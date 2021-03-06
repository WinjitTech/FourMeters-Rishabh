# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import numpy as np

import cv2


def zero_needle_position(img_path, iteration, meter_no, size):
    try:
        # Todo: Read Image
        image = cv2.imread(img_path + "\\MeterImages\\Crop\\" + str(meter_no) + "\\" + str(meter_no) + ".jpg", 0)
        # TODO: Find corner of needle
        if size == "meter72":
            x1 = 80
            x2 = 200
        if size == "meter96":
            x1 = 100
            x2 = 300
        color = int(image[270, 270])
        cv2.rectangle(image, (0, 0), (x1, 1000), (color, color, color), -1)
        cv2.rectangle(image, (x2, 0), (1000, 1000), (color, color, color), -1)
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


