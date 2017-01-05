# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import numpy as np

import cv2


def get_needle_tip(img_path, iteration):
    try:
        # print "Iteration", iteration
        image = cv2.imread(img_path + "\\MeterImages\\Needle.jpg", 0)
        color = int(image[270, 270])
        cv2.rectangle(image, (0, 0), (255, 600), (color, color, color), -1)
        cv2.rectangle(image, (0, 0), (500, 255), (color, color, color), -1)
        kernel = np.ones((5, 5), np.uint8)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        dilation = cv2.dilate(image, kernel, iterations=iteration)
        # ret, img = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
        # cv2.imshow("fd", dilation)
        corners = cv2.goodFeaturesToTrack(dilation, 2, 0.1, 10)
        # print "Corners", len(corners)
        cx = cy = 0
        for i in corners:
            x, y = i.ravel()
            # cv2.circle(dilation, (x, y), 2, (0, 255, 0), -1)
            cx += x
            cy += y
            # print "Co-ordinates: ", x, y
        cx /= len(corners)
        cy /= len(corners)
        # cv2.circle(dilation, (int(cx), int(cy)), 4, (0, 255, 0), -1)
        return cx, cy
    except Exception, e:
        # TODO: Call dilation again if Needle position in not found
        # dilute_image(top_x, base_y, 2)
        # print "Dilation Exception", str(e)
        return
