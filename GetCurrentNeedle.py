# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import cv2
import math
import numpy as np


def get_needle_tip(img_path, top_x, base_y, iteration):
    try:
        f = open(img_path + "\\Needlelog.txt", "a")
        image = cv2.imread(img_path + "\\MeterImages\\Needle.jpg", 0)
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(image, kernel, iterations=iteration)
        corners = cv2.goodFeaturesToTrack(dilation, 5, 0.1, 10)
        needle_len = []
        corner = 0
        for i in corners:
            x, y = i.ravel()

            n_lenght = math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2)
            if 400 < n_lenght < 450:
                needle_len.append(n_lenght)
                corner += 1
        if not needle_len:
            f.write("Failed")
            f.close()
            return
        needle_len.sort(reverse=True)

        for i in corners:
            x, y = i.ravel()
            n_lenght = math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2)
            if n_lenght == needle_len[0]:
                f.write("success")
                f.close()
                return x, y
        f.close()
    except Exception, e:
        # TODO: Call dilation again if Needle position in not found
        # print "Dilation Exception", str(e)
        # print "error"
        f.write("Needle Detection: " + str(e))
        f.close()
        return
