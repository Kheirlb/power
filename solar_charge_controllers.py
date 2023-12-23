from pymodbus.client import ModbusTcpClient
import time

def scale_f16(passed_val):
    s = 0  # sign
    e = 0  # exponent
    current_val = 0  # mantissa/result

    current_val = (passed_val & 0x03ff) / 1024.0  # 10 bit mantissa (normalized)
    passed_val >>= 10
    e = (passed_val & 0x001f)  # 5 bit exponent (stored w/ 15 offset)
    passed_val >>= 5
    s = passed_val & 0x0001  # 1 bit sign

    if e == 0:  # zero or subnormal
        if current_val == 0:
            return 0  # zero
        # else subnormal (no leading 1.xxx)
        current_val *= 2.0**(-14)
        if s != 0:
            current_val *= -1.0
        return current_val

    if e == 0x1f:  # infinity or NaN
        if current_val == 0:
            if s == 0:
                return float('inf')  # +infinity
            else:
                return float('-inf')  # -infinity
        else:
            return float('nan')  # NaN

    current_val += 1.0  # add in leading 1
    current_val *= 2.0**(e - 15)
    if s != 0:
        current_val *= -1.0

    return current_val

class SolarCharger:
    def __init__(self, ip, port=1025):
        self.client = ModbusTcpClient(ip, port)
        self.client.connect()

    def power_out(self):
        response = self.client.read_holding_registers(58, 1, 1)
        return scale_f16(response.registers[0])

sc1 = SolarCharger("192.168.1.101")
sc2 = SolarCharger("192.168.1.102")
sc3 = SolarCharger("192.168.1.103")
sc4 = SolarCharger("192.168.1.104")
sc5 = SolarCharger("192.168.1.105")
sc6 = SolarCharger("192.168.1.106")

while True:
    mb_power_out_1 = sc1.power_out()
    mb_power_out_2 = sc2.power_out()
    mb_power_out_3 = sc3.power_out()
    mb_power_out_4 = sc4.power_out()
    mb_power_out_5 = sc5.power_out()
    mb_power_out_6 = sc6.power_out()
    print(f"Solar Output #1: {mb_power_out_1:0.1f} W")
    print(f"Solar Output #2: {mb_power_out_2:0.1f} W")
    print(f"Solar Output #3: {mb_power_out_3:0.1f} W")
    print(f"Solar Output #4: {mb_power_out_4:0.1f} W")
    print(f"Solar Output #5: {mb_power_out_5:0.1f} W")
    print(f"Solar Output #6: {mb_power_out_6:0.1f} W")
    total_solar_output = mb_power_out_1 + mb_power_out_2 + mb_power_out_3 + mb_power_out_4 + mb_power_out_5 + mb_power_out_6
    print(f"Total Solar Output: {total_solar_output / 1000:0.4f} kW")
    time.sleep(1)
