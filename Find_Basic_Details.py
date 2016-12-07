import json
import math

import cv2
import GetCardinalContours
import GetBaseCardinals


def get_cardianls_from_image(meter_no, img_path, supression, min_range, max_range, iterate, size):
    meter_info = open(img_path + "\\MeterImages\\Crop\\" + str(meter_no) + "\\" + str(meter_no) + ".json", "w")
    meterinfo = {}
    cardinal_coordinates = []
    base_x, base_y = GetBaseCardinals.zero_needle_position(img_path, iterate, meter_no)

    # Todo: Generate all contours array
    contour_array = GetCardinalContours.get_contours(img_path, min_range, max_range, meter_no)

    # Todo: get top contours coordinates
    try:
        top_x, top_y = GetCardinalContours.find_top_cardinal(contour_array, min_range, max_range, supression, img_path,
                                                         meter_no)
    except Exception, e:
        print("In finding Top cardinal", str(e))
    min_dist = math.sqrt((top_x - top_x) ** 2 + (top_y - base_y) ** 2)

    # print "minimum dist", min_dist
    # TODO: Draw initial cardinal line
    img, cardinal_contour_list, cardinal_coordinates = GetCardinalContours.draw_main_cardinals(img_path, contour_array,
                                                                                               top_x, base_y, min_dist,
                                                                                               min_range, max_range,
                                                                                               meter_no, size)

    img = GetCardinalContours.draw_intermediate_cardinals(img, (base_x, base_y), top_x, top_y)
    cv2.imwrite(img_path + "\\MeterImages\\Crop\\" + str(meter_no) + "\\" + "cardinals.jpg", img)
    meterinfo["meter" + str(meter_no)] = {
            "base_x": str(base_x),
            "base_y": str(base_y),
            "top_x": str(top_x),
            "top_y": str(top_y),
            "cardinal_coordinates": cardinal_coordinates,
            "Total_cardinals_found": len(cardinal_coordinates)
        }
    meter_info.write(json.JSONEncoder().encode(meterinfo))
    meter_info.close()

