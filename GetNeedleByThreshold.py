# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import math

import numpy as np

import cv2


# TODO: Alternate method to detect needle


def get_needle_tip(img_path, top_x, base_y, iteration, meter_no):
    try:
        image = cv2.imread(img_path + "\\MeterImages\\Crop\\" + str(meter_no) + "\\Needle.jpg", 0)
        kernel = np.ones((5, 5), np.uint8)
        ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_OTSU)
        dilation = cv2.dilate(thresh, kernel, iterations=iteration)
        corners = cv2.goodFeaturesToTrack(dilation, 100, 0.1, 10)
        needle_len = []
        corner = 0
        for i in corners:
            x, y = i.ravel()
            cv2.circle(image, (x, y), 2, 255, -1)
            n_lenght = math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2)
            if 150 < n_lenght < 550:
                needle_len.append(n_lenght)
                corner += 1
        if not needle_len:
            return
        needle_len.sort(reverse=True)
        for i in corners:
            x, y = i.ravel()
            n_lenght = math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2)
            if n_lenght == needle_len[0]:
                # cv2.circle(dilation, (x, y), 10, (0, 0, 0), -1)
                # cv2.imshow("Needle Detection", dilation)
                # print "Needle length: ",n_lenght
                # cv2.waitKey(0)
                return x, y
    except Exception, e:
        print("In get_needle_tip", str(e))
        return


def get_needle_tip_for_sticky(img_path, top_x, base_y, iteration, meter_no, i):
    try:
        image = cv2.imread(img_path + "\\MeterImages\\Crop\\raw\\" + str(meter_no) + "\\" + str(i) + ".jpg", 0)
        kernel = np.ones((5, 5), np.uint8)
        ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_OTSU)
        dilation = cv2.dilate(thresh, kernel, iterations=iteration)
        corners = cv2.goodFeaturesToTrack(dilation, 100, 0.1, 10)
        needle_len = []
        corner = 0
        for i in corners:
            x, y = i.ravel()
            cv2.circle(image, (x, y), 2, 255, -1)
            n_lenght = math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2)
            if 150 < n_lenght < 550:
                needle_len.append(n_lenght)
                corner += 1
    # cv2.imshow("new", image)
        # cv2.waitKey(0)
        if not needle_len:
            print("Connot Detect Needle in sticky calculation")
            return
        needle_len.sort(reverse=True)
        for i in corners:
            x, y = i.ravel()
            n_lenght = math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2)
            if n_lenght == needle_len[0]:
                # cv2.circle(dilation, (x, y), 10, (0, 0, 0), -1)
                # cv2.imshow("Needle Detection", dilation)
                # # print "Needle length: ",n_lenght
                # cv2.waitKey(0)
                # cv2.imwrite(img_path + "\\MeterImages\\Dilate\\" + str(time.time()) + ".jpg", dilation)
                return x, y
    except ValueError:
        return