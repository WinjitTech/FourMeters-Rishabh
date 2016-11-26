# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <python file to return cardinal contours>


import cv2
import math
import numpy as np
import Find_Angle


def get_contours(img_path, min_range, max_range, meter_no):
    meter_image = cv2.imread(img_path+"\\Auto\\MeterImages\\Crop\\"+str(meter_no)+"\\"+str(meter_no)+".jpg")
    try:
        gray = cv2.cvtColor(meter_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_OTSU)
        try:
            _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        except ValueError:
            return
        cardinal = []
        # Todo: find contours area between cardinal points area in image

        for cnt in contours:
            # print "Outer: ", cv2.contourArea(cnt)
            if min_range <= cv2.contourArea(cnt) <= max_range:
                # print "Inner: ", cv2.contourArea(cnt)
                # (x, y), radius = cv2.minEnclosingCircle(cnt)
                # cv2.circle(meter_image, (int(x), int(y)), 10, (0, 255, 0), 5)
                cardinal.append(cnt)
        return cardinal
    except Exception, e:
        print "In get_contours method:", str(e)
        return


# TODO: Function to get contour at full deflection position contour
def find_top_cardinal(contours, min_range, max_range, supression, img_path, meter_no):
    image = cv2.imread(img_path+"\\Auto\\MeterImages\\Crop\\"+str(meter_no)+"\\"+str(meter_no)+".jpg")
    if supression == "x1":
        i = 0
        for cnt in contours:
            try:
                if min_range <= cv2.contourArea(cnt) <= max_range:
                    if i >= len(contours) - 1:
                        # print cv2.contourArea(cnt)
                        (x, y), radius = cv2.minEnclosingCircle(cnt)
                        c = cnt.ravel()
                        cx = c[::2]
                        cy = c[1::2]
                        top_x = int(round(sum(cx) / len(cx)))
                        top_y = int(round(sum(cy) / len(cy)))
                        top_x = (top_x + x) / 2
                        top_y = (top_y + y) / 2
                        # cv2.circle(image, (int(x), int(y)), 10, (0, 255, 0), 5)
                        # cv2.imshow("cvhj", image)
                        # cv2.waitKey(0)
                        return int(top_x), int(top_y)
                        # return x, y
                    i += 1
            except Exception, e:
                print "find_top_cardinal method in x1", str(e)
                continue

    if supression == "x2" or supression == 'x5':
        try:
            kernel = np.ones((5, 5), np.uint8)
            dilation = cv2.dilate(image, kernel, iterations=0)
            corners = cv2.goodFeaturesToTrack(dilation, 100, 0.1, 10)
            cx = cy = 0
            listy = []  # Todo : top x & y
            for i in corners:
                x, y = i.ravel()
                cv2.circle(dilation, (x, y), 2, (0, 255, 0), -1)
                cx += x
                cy += y
                listy.append(y)
            listy.sort()
            for i in corners:
                x, y = i.ravel()
                if y == listy[0]:
                    cv2.circle(dilation, (int(x), int(y)), 10, (0, 255, 0), -1)
                    x2 = x
                    y2 = y
                    break
            return x2, y2
        except Exception, e:
            print "In find_top_cardinal method in x2 or x2", str(e)


def draw_main_cardinals(img_path, contours, top_x, base_y, min_dist, min_range, max_range, meter_no, size):
    i = 0
    contour_list = []
    cardinal_cordinates = []
    meter = cv2.imread(img_path+"\\Auto\\MeterImages\\Crop\\"+str(meter_no)+"\\"+str(meter_no)+".jpg")
    try:
        for cnt in contours:
            # print "outer:", cv2.contourArea(cnt)
            if min_range <= cv2.contourArea(cnt) <= max_range:
                # TODO: Angle calculation between each contour
                c = cnt.ravel()
                cx = c[::2]
                cy = c[1::2]
                x = int(round(sum(cx) / len(cx)))
                y = int(round(sum(cy) / len(cy)))
                dist = math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2)
                # Todo: only compare distance of zero cardinal and five cardinal
                if size == "meter72":
                    sub = 35
                else:
                    sub = 45
                if min_dist - sub <= dist <= min_dist + sub:  # this is final dist >= min_dist - 25:
                    cv2.circle(meter, (int(x), int(y)), 2, 255, -1)
                    # print "Inner:", dist
                    cv2.line(meter, (int(x), int(y)), (int(top_x), int(base_y)), (255, 0, 0), 1)
                    cardinal_cordinates.append((x, y))
                    contour_list.append(cnt)
                    i += 1
        # print "cardinals", len(cardinal_cordinates)
    except Exception, e:
        print "In draw_main_cardinals method:", str(e)
        return
    return meter, contour_list, cardinal_cordinates


# Todo: Get pointer angle w.r.t. cardinals
def get_needle_angles(top_x, base_y, pointer, base_line, cardinal_coordinates):
    angle_list = []
    cardinal_angle = []
    # print "Total no of cardinals: ", skip_last_cardinal
    try:
        for x, y in cardinal_coordinates:
            cardinal = ((float(x), float(y)), (top_x, base_y))
            cardinal_ang = round(Find_Angle.ang(cardinal, base_line), ndigits=2)
            cardinal_angle.append(cardinal_ang)
            base_and_pointer_angle = Find_Angle.ang(base_line, pointer)
            needle_angle = Find_Angle.ang(cardinal, pointer)
            if base_and_pointer_angle >= cardinal_ang:
                angle_list.append(round(needle_angle, ndigits=2))
            else:
                angle_list.append(round(-needle_angle, ndigits=2))
            # print "from ang", len(angle_list)
            # print angle_list
        return angle_list, cardinal_angle
    except Exception, e:
        print "In get_needle_angles method:", str(e)
        return


def draw_intermediate_cardinals(meter, base_contour, top_x, top_y):
    try:
        (base_x, base_y) = base_contour
        # (top_x, top_y), radius = cv2.minEnclosingCircle(topcontour)
        cv2.line(meter, (int(base_x), int(base_y)), (int(top_x), int(base_y)), (0, 0, 255), 1)
        cv2.line(meter, (int(top_x), int(top_y)), (int(top_x), int(base_y)), (0, 0, 255), 1)
        return meter
    except Exception, e:
        print "In draw_intermediate_cardinals method ", str(e)
        return

