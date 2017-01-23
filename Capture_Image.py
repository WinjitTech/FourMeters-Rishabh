# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

from MainProcess import *
import cv2


def start_capture(meter, cardinal_number, img_name, img_path, mod_factor, size, suppression, cardinal_len, cursor,
                  updown):
    frames_json = open(img_path + "\\MeterImages\\Crop\\frame.json")
    data = json.load(frames_json)
    frames_json.close()
    try:
        for meter_no in data:
            meter_crop = json.loads(data[meter_no])
            x1 = meter_crop.get("x1")
            x2 = meter_crop.get("x2")
            y1 = meter_crop.get("y1")
            y2 = meter_crop.get("y2")
            cropped_meter = meter[y1:y2, x1:x2]
            # cv2.imshow(str(meter_no), cropped_meter)
            # cv2.waitKey(0)
            cv2.imwrite(img_path + "\\MeterImages\\Crop\\" + str(meter_no) + "\\Needle.jpg", cropped_meter)
            try:

                m, angles, deflections = initprocess(img_path, cropped_meter, mod_factor, size, meter_no)
                angle = round(angles[cardinal_number - 1], ndigits=4)
                deflection = round(deflections[cardinal_number - 1], ndigits=4)
                print(angle, deflection)
                cv2.imwrite(
                    img_path + '\\MeterImages\\Crop\\' + str(meter_no) + "\\" + str(img_name) + ".jpg", m)
                sql_query = "insert into AngleDeflectionReadings (MeterNo, CardinalNo, Angle, Deflection,UpDown) values(" + str(
                    meter_no) + "," + str(cardinal_number) + "," + str(angle) + "," + str(deflection) + "," + str(
                    updown) + ");"
                cursor.execute(sql_query)
            except Exception, e:
                print("from initprocess", str(e))
    except Exception, e:
        print("In Capture Image", str(e))
