# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import math


def dot(vA, vB):
    return vA[0] * vB[0] + vA[1] * vB[1]


def ang(lineA, lineB):
    try:
        # Get nicer vector form
        vA = [(lineA[0][0] - lineA[1][0]), (lineA[0][1] - lineA[1][1])]
        vB = [(lineB[0][0] - lineB[1][0]), (lineB[0][1] - lineB[1][1])]
        # Get dot prod
        dot_prod = dot(vA, vB)
        # Get magnitudes
        magA = dot(vA, vA) ** 0.5
        magB = dot(vB, vB) ** 0.5
        # Get cosine value
        cos_ = dot_prod / magA / magB
        # Get angle in radians and then convert to degrees
        angle = math.acos(dot_prod / magB / magA)
        # Basically doing angle <- angle mod 360
        ang_deg = round(math.degrees(angle) % 360, ndigits=4)

        if ang_deg - 180 >= 0:
            # As in if statement
            return 360 - ang_deg
            # else:
    except Exception, e:
        # print str("ang", e)
        # print "error"
        return
    return ang_deg
