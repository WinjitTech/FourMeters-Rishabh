__author__ = 'RohitSalunke'

import json
import sys
import cv2
import imutils
import Find_Basic_Details
import math
import GetCardinalContours
import GetBaseCardinals

# from Capture_Image import *

# def calibration(img_path, size, supression):
if len(sys.argv) > 1:
    f = open("C:\\ProgramData\\Rishabh\\Auto\\calibrate.txt", "w")
    f.write(str(sys.argv))
    f.close()
    img_path = str(sys.argv[1])
    size = "meter" + str(sys.argv[2])
    supression = str(sys.argv[3])
else:
    # img_path = "C:\\Users\\rohitsalunke\\PycharmProjects\\RishabhWebCam\\Auto Program"
    # img_path = "C:\\ProgramData\\Rishabh\\Auto"
    size = "meter96"
    supression = "x1"

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.set(3, 2592)
cap.set(4, 2048)
config = open("C:\\ProgramData\\Rishabh\\Auto\\rishabh.config", "r")
json_data = json.load(config)
img_path = json_data["img_path"]
# config.close()
if not ret:
    print ("Check if Camera is Available")
    cap.release()
    cv2.destroyAllWindows()
else:
    data = {}
    config = open(img_path + "\\Auto\\frame.json", "w")
    # config = open("frame.json", "w")
    cam_status = open(img_path + "\\Auto\\camerastatus.txt", "w")
    cam_status.write("true")
    cam_status.close()
    # cam_status = open("camerastatus.txt", "w")
    msg = "Press 'Esc' or 'space' button to proceed..."

    meter_crop = open(img_path + "\\Auto\\cropping.json", "r")
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
            # img_show = image
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
                resized_image = cv2.resize(image, (1024, 900))
                cv2.imshow("Meter", resized_image)
                meter_frame = {}
                meter_no = 0
                config = open(img_path + "\\Auto\\MeterImages\\crop\\frame.json", "w")
                json_data = ""
                meter_obj = {}
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
                                cv2.rectangle(image, (int(x + x1), int(y + y1)), (int((w + x) - x2), int(h + y) - y2),
                                              (0, 255, 0), thickness=2)
                                cv2.rectangle(image, (int(x), int((y))), (int((w + x)), int(h + y)), (0, 255, 0),
                                              thickness=2)
                                meter_frame = image[int(y + y1 + 2):int(h + y) - y2 - 2,
                                              int(x + x1 + 2):int(w + x) - x2 - 2]
                                cv2.putText(image, msg, (20, 20), cv2.QT_FONT_NORMAL, 0.5, (0, 255, 0), thickness=1,
                                            lineType=cv2.CV_8U)
                                resized_image = cv2.resize(image, (1024, 900))
                                cv2.putText(image, msg, (20, 20), cv2.QT_FONT_NORMAL, 0.5, (0, 255, 0), thickness=1,
                                            lineType=cv2.CV_8U)
                                cv2.imshow("Meter", resized_image)
                                data["x1"] = int(x + x1 + 2)
                                data["x2"] = int(w + x) - x2 - 2
                                data["y1"] = int(y + y1 + 2)
                                data["y2"] = int(h + y) - y2 - 2
                                # Todo: generate cropping property for number of meters on gig
                                meter_obj[meter_no + 1] = json.dumps(data)
                                meter_no += 1
                                cv2.imwrite(
                                    img_path + "\\Auto\\MeterImages\\crop\\" + str(meter_no) + "\\" + str(meter_no) + ".jpg",
                                    meter_frame)
                if cv2.waitKey(1) & 0xFF == ord(' '):
                    cap.release()
                    cv2.destroyAllWindows()
                    break
                if cv2.waitKey(1) == 27:
                    cap.release()
                    cv2.destroyAllWindows()
                    break
    except Exception, e:
        cap.release()
        cv2.destroyAllWindows()
        print str(e)
    meter_obj = json.JSONEncoder().encode(meter_obj)
    config.write(meter_obj)
    config.close()
    cam_status = open(img_path + "\\camerastatus.txt", "w")
    cam_status.write("true")
    cam_status.close()
    meter_size = open(img_path + "\\Auto\\metersize.json", "r")
    json_data = json.load(meter_size)
    min_range = json_data[size]["min_range"]
    max_range = json_data[size]["max_range"]
    # print min_range, max_range
    meter_size.close()

    # meter_info = open(img_path + "\\Auto\\MeterImages\\crop\\meterinfo.json", "w")
    # meterinfo = {}
    if size == "meter48":
        iterate = 4
    else:
        iterate = 3
    while meter_no != 0:
        Find_Basic_Details.get_cardianls_from_image(meter_no, img_path, supression, min_range, max_range, iterate, size)
        # exit()
        meter_no -= 1

# calibration(img_path, size, supression)
