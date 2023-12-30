from pymodbus.client import ModbusTcpClient
from influxdb_client import Point

# Helper function to read float values from solar charge controller.
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
        # TODO(kparks): Handle error better.
        return float(scale_f16(response.registers[0])) / 1000.0

def connect():
    sc1 = SolarCharger("192.168.1.101")
    sc2 = SolarCharger("192.168.1.102")
    sc3 = SolarCharger("192.168.1.103")
    sc4 = SolarCharger("192.168.1.104")
    sc5 = SolarCharger("192.168.1.105")
    sc6 = SolarCharger("192.168.1.106")
    return (sc1, sc2, sc3, sc4, sc5, sc6)

def get_point(name, solar_output):
    print(f"{name}: \t{solar_output:0.1f} kW")
    return (
        Point(name)
        .field("power_kw", solar_output)
    )

def get_points(sc1, sc2, sc3, sc4, sc5, sc6):
    mb_power_out_1 = sc1.power_out()
    mb_power_out_2 = sc2.power_out()
    mb_power_out_3 = sc3.power_out()
    mb_power_out_4 = sc4.power_out()
    mb_power_out_5 = sc5.power_out()
    mb_power_out_6 = sc6.power_out()
    point1 = get_point("solar_charger_1", mb_power_out_1)
    point2 = get_point("solar_charger_2", mb_power_out_2)
    point3 = get_point("solar_charger_3", mb_power_out_3)
    point4 = get_point("solar_charger_4", mb_power_out_4)
    point5 = get_point("solar_charger_5", mb_power_out_5)
    point6 = get_point("solar_charger_6", mb_power_out_6)
    total_solar_output = mb_power_out_1 + mb_power_out_2 + mb_power_out_3 + mb_power_out_4 + mb_power_out_5 + mb_power_out_6
    # Sometimes the solar charge controllers read a tiny bit of power even in the middle of the night.
    # If they total less than 10 watts, we set the total to 0.0 so it is not as distracting.
    if total_solar_output < 0.010:
        total_solar_output = 0.0
    point_total = get_point("solar_charger_total", total_solar_output)
    return [point1, point2, point3, point4, point5, point5, point6, point_total]
