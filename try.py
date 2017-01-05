import time

import serial

__author__ = 'RohitSalunke'


class Calmet:
    def __init__(self):
        ser = serial.Serial('COM5', baudrate=4800, timeout=1)
        self.GetDetails(ser)

    def GetDetails(self, ser):
        no_of_cardinals = int(raw_input("Enter No of cardinals: "))
        fsd = float(raw_input("Enter FSD: "))
        electrical_parameter = str(raw_input("Enter Electrical Parameter(mv/volts/ma/ampere): ").lower())
        frequency = str(raw_input("Enter Frequency(dc/50/60/400/fext): ").lower())
        self.setVariables(ser, no_of_cardinals, fsd, electrical_parameter, frequency)

    def setVariables(self, ser, no_of_cardinals, fsd, electrical_parameter, frequency):
        if "mv" in electrical_parameter:
            electrical_parameter = "Z0"
        if "vo" in electrical_parameter:
            if fsd <= 2:
                electrical_parameter = "Z1"
            if 2 < fsd <= 20:
                electrical_parameter = "Z2"
            if 20 < fsd <= 200:
                electrical_parameter = "Z3"
            if fsd > 200:
                electrical_parameter = "Z4"

        if "ma" in electrical_parameter:
            if fsd <= 1:
                electrical_parameter = "Z5"
            if 1 < fsd <= 10:
                electrical_parameter = "Z6"
            if 10 < fsd <= 100:
                electrical_parameter = "Z7"
        if "amp" in electrical_parameter:
            if fsd <= 1:
                electrical_parameter = "Z8"
            if fsd > 1:
                electrical_parameter = "Z9"
        if "dc" in frequency:
            frequency = "F0"
        if "50" in frequency:
            frequency = "F1"
        if "60" in frequency:
            frequency = "F2"
        if "400" in frequency:
            frequency = "F3"
        if "fext" in frequency:
            frequency = "F4"
        current_voltage = fsd
        next_voltage = fsd / no_of_cardinals
        arr_cardinals = [str(fsd)]
        for i in range(0, no_of_cardinals):
            current_voltage -= next_voltage
            arr_cardinals.append(str(current_voltage))
        del arr_cardinals[-1]
        current_voltage = fsd
        if no_of_cardinals == 4:
            rate = 80
        else:
            rate = 90
        step = (fsd / rate)
        s = '\x02Z0,F1,N00.00000,O\x03'
        # ser.write(s)
        time.sleep(0.1)
        ser.write('\x02' + str(electrical_parameter) + "," + str(frequency) + '\x03')
        time.sleep(0.5)
        ser.write("\x02O\x03")
        time.sleep(0.3)
        ser.write('\x02K\x03')
        time.sleep(0.1)
        self.updown(ser, current_voltage, step, arr_cardinals, no_of_cardinals)
        self.downup(ser, fsd, step, arr_cardinals, no_of_cardinals=1)
        self.reset(ser)

    def updown(self, ser, current_voltage, step, arr_cardinals, no_of_cardinals):
        ser.write("\x02O\x03")
        time.sleep(0.3)
        ser.write('\x02K\x03')
        time.sleep(0.1)
        current_voltage += step * 2
        # Todo: start up cycle
        while current_voltage > 0:
            current_voltage -= step
            time.sleep(0.04)
            ser.write('\x02N' + str(current_voltage) + '\x03')
            time.sleep(0.04)
            if str(current_voltage) in arr_cardinals:
                print "Current_Voltage up-down", current_voltage, "Cardinal No.", no_of_cardinals
                time.sleep(0.5)
                no_of_cardinals -= 1
                # Todo: Call cardinal angle and needle angle detection here for up/down
        time.sleep(0.1)
        ser.write('\x02K\x03')
        time.sleep(0.1)
        ser.write('\x02')
        ser.write('N' + str(0))
        ser.write('\x03')
        time.sleep(1)
        ser.write('\x02K\x03')
        time.sleep(0.1)

    def downup(self, ser, fsd, step, arr_cardinals, no_of_cardinals):
        current_voltage = 0
        # Todo: start downup cycle
        while current_voltage <= fsd + step:
            current_voltage += step
            time.sleep(0.04)
            ser.write('\x02N' + str(current_voltage) + '\x03')
            time.sleep(0.04)
            if str(current_voltage) in arr_cardinals:
                print "Current_Voltage down-up", current_voltage, "Cardinal No.", no_of_cardinals
                time.sleep(0.5)
                no_of_cardinals += 1
                # Todo: Call cardinal angle and needle angle detection here for up/down
        time.sleep(0.1)
        ser.write('\x02K\x03')
        time.sleep(0.1)
        ser.write('\x02N0.0000\x03')
        time.sleep(0.1)
        ser.write('\x020\x03')
        time.sleep(0.1)
        ser.write('\x02S\x03')
        time.sleep(0.1)
        ser.write('\x02K\x03')
        time.sleep(0.1)

    def reset(self, ser):
        ser.write('\x020\x03')
        time.sleep(0.1)
        ser.write('\x02S\x03')
        time.sleep(0.1)
        ser.write('\x02K\x03')
        time.sleep(0.1)


if __name__ == "__main__":
    Calmet()
