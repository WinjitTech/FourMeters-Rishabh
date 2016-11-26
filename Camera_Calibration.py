# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import json
import sys
import cv2
import imutils
import math

import time

import GetCardinalContours
import GetBaseCardinals

# def calibration(img_path, size, supression):
if len(sys.argv) > 1:
    f = open("C:\\ProgramData\\Rishabh\\Auto\\calibrate.txt", "w")
    f.write(str(sys.argv))
    f.close()
    img_path = str(sys.argv[1])
    size = "meter" + str(sys.argv[2])
    supression = str(sys.argv[3])
else:
    img_path = "C:\\Users\\rohitsalunke\\PycharmProjects\\RishabhWebCam\\Auto Program"
    # img_path = "C:\\ProgramData\\Rishabh\\Auto"
    size = "meter96"
    supression = "x2"

#
cap = cv2.VideoCapture(0)
# time.sleep(1))

ret, frame = cap.read()

if not ret:
    print ("Check if Camera is Available")
    cap.release()
    cv2.destroyAllWindows()
else:
    data = {}
    config = open(img_path + "\\frame.json", "w")
    # config = open("frame.json", "w")
    cam_status = open(img_path + "\\camerastatus.txt", "w")
    cam_status.write("true")
    cam_status.close()
    # cam_status = open("camerastatus.txt", "w")
    msg = "Press 'Esc' or 'space' button to proceed..."

    meter_crop = open(img_path + "\\cropping.json", "r")
    json_data = json.load(meter_crop)
    x1 = json_data[size]["x1"]
    y1 = json_data[size]["y1"]
    x2 = json_data[size]["x2"]
    y2 = json_data[size]["y2"]
    rx1 = json_data[size]["rec_x1"]
    ry1 = json_data[size]["rec_y1"]
    rx2 = json_data[size]["rec_x2"]
    ry2 = json_data[size]["rec_y2"]
    meter_crop.close()
    try:
        while 1:
        # for i in range(0, 10):
            ret, image = cap.read()
            ret, image = cap.read()
            ret, image = cap.read()
            img_show = image
            if not ret:
                print ("Check if Camera is Available")
            else:
                # cv2.rectangle(img_show, (342, 172), (882, 700), (0, 255, 0), thickness=2)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                #
                # cv2.putText(image, msg, (80, 80), cv2.QT_FONT_NORMAL, 0.5, (0, 255, 0), thickness=1,
                #             lineType=cv2.CV_8U)
                cv2.rectangle(img_show, (rx1, ry1), (rx2 + rx1, ry2 + ry1), (0, 255, 0), thickness=2)
                cv2.imshow("Meter", image)
                for c in cnts:
                    M = cv2.moments(c)
                    cX = int((M["m10"]))
                    cY = int((M["m01"]))
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
                    if len(approx) == 4:
                        (x, y, w, h) = cv2.boundingRect(approx)
                        ar = w / float(h)
                        shape = "square"
                        if 0.95 <= ar <= 1.05:
                            if cv2.contourArea(c) > 40000:
                                (x, y, w, h) = cv2.boundingRect(approx)
                                (cx, cy), radius = cv2.minEnclosingCircle(approx)
                                # cv2.rectangle(img_show, (300, 130), (685 + 300, 690 + 130), (0, 255, 0), thickness=2)
                                # cv2.rectangle(image, (int(x), int(y)), (int(w + x), int(h + y)), (0, 255, 0),
                                #  thickness=2)
                                # cv2.rectangle(image, (int(x + 32), int(y + 32)), (int((w + x) - 106), int(h + y) - 106),
                                #               (0, 255, 0), thickness=2)
                                # meter_frame = image[int(y + 34):int(h + y) - 108, int(x + 34):int(w + x) - 108]
                                cv2.rectangle(image, (int(x + x1), int(y + y1)),
                                              (int((w + x) - x2), int(h + y) - y2),
                                              (0, 255, 0), thickness=2)
                                meter_frame = image[int(y + y1 + 2):int(h + y) - y2 - 2,
                                              int(x + x1 + 2):int(w + x) - x2 - 2]

                                data["x1"] = int(x + x1 + 2)
                                data["x2"] = int(w + x) - x2 - 2
                                data["y1"] = int(y + y1 + 2)
                                data["y2"] = int(h + y) - y2 - 2
                                cv2.putText(image, msg, (20, 20), cv2.QT_FONT_NORMAL, 0.5, (0, 255, 0), thickness=1,
                                            lineType=cv2.CV_8U)
                                cv2.imshow("Meter", img_show)
                                # print int(y + 40), int(h + y) - 100, int(x + 40), int(w + x) - 100
                if cv2.waitKey(1) & 0xFF == ord(' '):
                    cap.release()
                    cv2.destroyAllWindows()
                    break
                if cv2.waitKey(1) == 27:
                    cap.release()
                    cv2.destroyAllWindows()
                    break

    except ValueError:
        cap.release()
        cv2.destroyAllWindows()
        # print str(e)
        print "error"
    json_data = json.dumps(data)
    # print json_data
    config.write(json_data)

    config.close()
    cv2.imwrite(img_path + "\\MeterImages\\cardinal.jpg", meter_frame)

    meter_size = open(img_path + "\\metersize.json", "r")
    json_data = json.load(meter_size)
    min_range = json_data[size]["min_range"]
    max_range = json_data[size]["max_range"]
    # print min_range, max_range
    meter_size.close()
    if size == "meter48":
        iterate = 4
    else:
        iterate = 3
    base_x, base_y = GetBaseCardinals.zero_needle_position(img_path, iterate)
    # base_x, base_y, top_x, top_y = GetBaseCardinals.zero_needle_position(img_path, 0)

    # Todo: Generate all contours array
    contour_array = GetCardinalContours.get_contours(img_path, min_range, max_range)
    # print "Cardinals Detected: ", len(contour_array)

    if supression == "x2" or supression == "x5":
        # Todo: supression cardinals length should
        skip_last_cardinal = len(contour_array)
    # else:
    #     # Todo: skip last cardinal for getting plot on Image if meter is x1
    #     skip_last_cardinal = len(contour_array) - 1

    # Todo: get top contours coordinates
    try:
        top_x, top_y = GetCardinalContours.find_top_cardinal(contour_array, min_range, max_range, supression, img_path)

        # Todo: get top contour distance
        # min_dist = math.sqrt((base_x - top_x) ** 2 + (base_y - top_y) ** 2)
        # print "minimum dist", min_dist

        min_dist = math.sqrt((top_x - top_x) ** 2 + (top_y - base_y) ** 2)

        # print "minimum dist", min_dist
        # TODO: Draw initial cardinal line
        img, cardinal_contour_list, cardinal_coordinates = GetCardinalContours.draw_main_cardinals(meter_frame,
                                                                                                   contour_array, top_x,
                                                                                                   base_y, min_dist,
                                                                                                   min_range, max_range,
                                                                                                   skip_last_cardinal,
                                                                                                   size)
        img = GetCardinalContours.draw_intermediate_cardinals(meter_frame, (base_x, base_y), top_x, top_y)
        # cv2.imwrite(img_path + "\\MeterImages\\cardinals.jpg", img)

        # Todo: Generate all contours array
        cv2.imwrite(img_path + "\\MeterImages\\cardinals.jpg", meter_frame)
        # cv2.imshow("temp", img)
        # cv2.waitKey(0)
        cam_status.close()
        cap.release()
        cv2.destroyAllWindows()
    except Exception, e:
        print "find top card:", str(e)


# calibration(img_path, size, supression)
