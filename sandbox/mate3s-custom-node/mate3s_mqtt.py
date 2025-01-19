import sunspec2.modbus.client as mate3s_client
import time
from signals import Signal

# TCP Device config
device_config = {
    "ipaddr": "192.168.1.100",
    "ipport": 1025,
    "scan_freq_s": "5"
}

# Publish config
# If more then one point_name is provided, add them together (useful for L1 and L2 things)
# If inverter_sum is true, add all values together (useful for multiple inverters).

signals_to_publish = {
    "battery_voltage": {
        "model_name": "inverter",
        "point_names": ["DCV"],
    },
    "total_output_current": {
        "model_name": "model_64115",
        "point_names": ["GS_Split_L1_Inverter_Output_Current", "GS_Split_L2_Inverter_Output_Current"],
        "inverter_sum": True,
    },
    "total_charge_current": {
        "model_name": "model_64115",
        "point_names": ["GS_Split_L1_Inverter_Charge_Current", "GS_Split_L2_Inverter_Charge_Current"],
        "inverter_sum": True,
    },
    "total_output_power_kw": {
        "model_name": "model_64115",
        "point_names": ["GS_Split_Output_kW"],
        "inverter_sum": True,
    },
    "total_charge_power_kw": {
        "model_name": "model_64115",
        "point_names": ["GS_Split_Charge_kW"],
        "inverter_sum": True,
    },
    "total_load_power_kw": {
        "model_name": "model_64115",
        "point_names": ["GS_Split_Load_kW"],
        "inverter_sum": True,
    }
}

# d = mate3s_client.SunSpecModbusClientDeviceTCP(ipaddr="192.168.1.100", ipport=1025)
d = mate3s_client.SunSpecModbusClientDeviceTCP(ipaddr=device_config["ipaddr"], ipport=device_config["ipport"])

while True:
    # Scan for new data.
    d.scan()

    # TODO(kparks): return some signals

    for key, signal in signals_to_publish.items():
        model_name = signal["model_name"]
        # TODO(kparks): Maybe don't assume every value is a float.
        total_value = 0.0
        for model_entry in d[model_name]:
            for point_name in signal["point_names"]:
                individual_value = float(model_entry[point_name].cvalue)
                total_value = individual_value

    time.sleep(device_config["scan_freq_s"])
