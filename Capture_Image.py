# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

from MainProcess import *
import cv2


def start_capture(meter, cardinal_number, img_name, img_path, mod_factor, size, suppression, cardinal_len):
    frames_json = open(img_path + "\\Auto\\MeterImages\\Crop\\frame.json")
    data = json.load(frames_json)
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
            cv2.imwrite(img_path + "\\Auto\\MeterImages\\Crop\\" + str(meter_no) + "\\Needle.jpg", cropped_meter)
            try:
                # meter, angles, deflection, top_x, base_y, base_x, base_y = initprocess(img_path, cropped_meter, mod_factor,
                #                                                                    size,
                #                                                                    suppression, cardinal_len, meter_no)
                m = initprocess(img_path, cropped_meter, mod_factor, size, suppression, cardinal_len, meter_no)
                # print(meter_no, angles)
                cv2.imwrite(img_path + '\\Auto\\MeterImages\\Crop\\' + str(meter_no)+"\\"+str(cardinal_number)+".jpg", m)
                # print(img_path + '\\Auto\\MeterImages\\Crop\\' + str(meter_no)+"\\"+str(cardinal_number)+".jpg")

            except Exception, e:
                print("from initprocess", str(e))

        # return str(angles[cardinal_number - 1]), str(deflection[cardinal_number - 1]), top_x, base_y, base_x, base_y
    except Exception, e:
        print(str(e))

    # try:
    #     meter, angles, deflection, top_x, base_y, base_x, base_y = initprocess(img_path, meter, mod_factor, size,
    #                                                                            suppression, cardinal_len)
    #     cv2.imwrite(img_path + '\\MeterImages\\' + img_name, meter)
    #     print angles
    #     return str(angles[cardinal_number - 1]), str(deflection[cardinal_number - 1]), top_x, base_y, base_x, base_y
    # except Exception, e:
    #     print "Capture Image in start_caputre: rec Image", str(e)
