import sunspec2.modbus.client as mate3s_client
from influxdb_client import Point

# Setup connection to mate3s
def connect():
    return mate3s_client.SunSpecModbusClientDeviceTCP(ipaddr="192.168.1.100", ipport=1025)

def inverter_64115(block):
    port = block.GS_Split_Port_number.value
    l1_output_a = float(block.GS_Split_L1_Inverter_Output_Current.cvalue)
    l1_charge_a = float(block.GS_Split_L1_Inverter_Charge_Current.cvalue)
    l2_output_a = float(block.GS_Split_L2_Inverter_Output_Current.cvalue)
    l2_charge_a = float(block.GS_Split_L2_Inverter_Charge_Current.cvalue)
    battery_v = float(block.GS_Split_Battery_Voltage.cvalue)
    output_kw = float(block.GS_Split_Output_kW.cvalue)
    charge_kw = float(block.GS_Split_Charge_kW.cvalue)
    load_kw = float(block.GS_Split_Load_kW.cvalue)
    # print("port", port)
    # print(l1_output_a)
    # print(l1_charge_a)
    # print(l2_output_a)
    # print(l2_charge_a)
    # print(battery_v)
    # print(output_kw)
    # print(charge_kw)
    # print(load_kw)
    return (
        Point(f"inverter-{port}")
        .field("l1_output_a", l1_output_a)
        .field("l1_charge_a", l1_charge_a)
        .field("l2_output_a", l2_output_a)
        .field("l2_charge_a", l2_charge_a)
        .field("battery_v", battery_v)
        .field("output_kw", output_kw)
        .field("charge_kw", charge_kw)
        .field("load_kw", load_kw)
    )

def add_values(block1, block2, block3, value_name):
    return  float(block1.points[value_name].cvalue) + float(block2.points[value_name].cvalue) + float(block3.points[value_name].cvalue)

def add_current_values(block1, block2, block3, value_name_1, value_name_2):
    return add_values(block1, block2, block3, value_name_1) + add_values(block1, block2, block3, value_name_2)

def get_points(d):
    d.scan()
    # Block 102
    inverter = d.inverter[0]
    battery_voltage = inverter.DCV.cvalue
    inverter_current = inverter.A.value
    power_usage = inverter.W.value
    print(f"Inverter Current: \t{inverter_current} \tAmps")
    print(f"Battery Voltage: \t{battery_voltage} \tVolts")
    print(f"Power Usage: \t\t{power_usage} \tW")
    old_point = (
        Point("mate3s")
        .field("Inverter Current", inverter_current)
        .field("Battery Voltage", battery_voltage)
        .field("Power Usage", power_usage)
    )

    # Block 64115 (multiple inverters)
    inverter1 = d.model_64115[0]
    inverter2 = d.model_64115[1]
    inverter3 = d.model_64115[2]
    # point1 = inverter_64115(inverter1)
    # point2 = inverter_64115(inverter2)
    # point3 = inverter_64115(inverter3)        

    total_output_current = add_current_values(inverter1, inverter2, inverter3, "GS_Split_L1_Inverter_Output_Current", "GS_Split_L2_Inverter_Output_Current")
    total_charge_current = add_current_values(inverter1, inverter2, inverter3, "GS_Split_L1_Inverter_Charge_Current", "GS_Split_L2_Inverter_Charge_Current")
    total_output_power = add_values(inverter1, inverter2, inverter3, "GS_Split_Output_kW")
    total_charge_power = add_values(inverter1, inverter2, inverter3, "GS_Split_Charge_kW")
    total_load_power = add_values(inverter1, inverter2, inverter3, "GS_Split_Load_kW")
    total = (
        Point("power_room_totals")
        .field("total_output_current", total_output_current)
        .field("total_charge_current", total_charge_current)
        .field("battery_voltage", battery_voltage)
        .field("total_output_power_kw", total_output_power)
        .field("total_charge_power_kw", total_charge_power)
        .field("total_load_power_kw", total_load_power)
    )
    # points = [old_point, point1, point2, point3, total]
    return [old_point, total]
