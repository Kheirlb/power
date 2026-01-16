import time
import sunspec2.modbus.client as mate3s_client

def connect():
    """Connect to the Mate3s Sunspec Modbus TCP client."""
    return mate3s_client.SunSpecModbusClientDeviceTCP(ipaddr="192.168.1.100", ipport=1025)

def inverter_64115(block, ts_ms):
    """Extract data from a Model 64115 Sunspec block."""
    port = block.GS_Split_Port_number.value
    l1_output_a = float(block.GS_Split_L1_Inverter_Output_Current.cvalue)
    l1_charge_a = float(block.GS_Split_L1_Inverter_Charge_Current.cvalue)
    l2_output_a = float(block.GS_Split_L2_Inverter_Output_Current.cvalue)
    l2_charge_a = float(block.GS_Split_L2_Inverter_Charge_Current.cvalue)
    battery_v = float(block.GS_Split_Battery_Voltage.cvalue)
    output_kw = float(block.GS_Split_Output_kW.cvalue)
    charge_kw = float(block.GS_Split_Charge_kW.cvalue)
    load_kw = float(block.GS_Split_Load_kW.cvalue)
    return {
        "ts_ms": ts_ms,
        "port": port,
        "l1_output_a": l1_output_a,
        "l1_charge_a": l1_charge_a,
        "l2_output_a": l2_output_a,
        "l2_charge_a": l2_charge_a,
        "battery_v": battery_v,
        "output_kw": output_kw,
        "charge_kw": charge_kw,
        "load_kw": load_kw,
    }

def add_values(block1, block2, block3, value_name):
    """Add values from three Sunspec blocks for a given value name."""
    return  float(block1.points[value_name].cvalue) + float(block2.points[value_name].cvalue) + float(block3.points[value_name].cvalue)

def add_current_values(block1, block2, block3, value_name_1, value_name_2):
    """Add current values from three Sunspec blocks for two given value names."""
    return add_values(block1, block2, block3, value_name_1) + add_values(block1, block2, block3, value_name_2)

def get_mqtt_data(d):
    """Get data formatted for MQTT publishing."""
    d.scan()
    ts_ms = int(time.time() * 1000)
    # Block 102 (need for just battery voltage I think)
    inverter = d.inverter[0]
    battery_voltage = inverter.DCV.cvalue
    # Block 64115 (multiple inverters)
    inverter1 = d.model_64115[0]
    inverter2 = d.model_64115[1]
    inverter3 = d.model_64115[2]
    inverter1_message = inverter_64115(inverter1)
    inverter2_message = inverter_64115(inverter2)
    inverter3_message = inverter_64115(inverter3)
    total_output_current = add_current_values(inverter1, inverter2, inverter3, "GS_Split_L1_Inverter_Output_Current", "GS_Split_L2_Inverter_Output_Current")
    total_charge_current = add_current_values(inverter1, inverter2, inverter3, "GS_Split_L1_Inverter_Charge_Current", "GS_Split_L2_Inverter_Charge_Current")
    total_output_power = add_values(inverter1, inverter2, inverter3, "GS_Split_Output_kW")
    total_charge_power = add_values(inverter1, inverter2, inverter3, "GS_Split_Charge_kW")
    total_load_power = add_values(inverter1, inverter2, inverter3, "GS_Split_Load_kW")
    totals_message = {
        "ts_ms": ts_ms,
        "total_output_current": total_output_current,
        "total_charge_current": total_charge_current,
        "battery_voltage": battery_voltage,
        "total_output_power_kw": total_output_power,
        "total_charge_power_kw": total_charge_power,
        "total_load_power_kw": total_load_power,
    }

    return [
        totals_message,
        inverter1_message,
        inverter2_message,
        inverter3_message
    ]
