"""
Power Room battery voltage and precent
Date created: 11/30/2024
Nick & Karl
"""

import time
import board
import busio
import json
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import paho.mqtt.client as mqtt

# We had ChatGPT write this for us to save us time.
def interpolate(x_table, y_table, x):
    """
    Perform linear interpolation for a given x using a table of x and y values.

    Args:
        x_table (list of float): Sorted list of x-values.
        y_table (list of float): Corresponding y-values.
        x (float): The x-value at which to interpolate.

    Returns:
        float: The interpolated y-value, or None if x is out of range.
    """
    if len(x_table) != len(y_table):
        raise ValueError("x_table and y_table must have the same length.")

    # Ensure x is within the range of x_table
    if x < x_table[0] or x > x_table[-1]:
        print("Error: voltage is out of range.")
        return 0

    # Find the interval [x0, x1] where x0 <= x < x1
    for i in range(len(x_table) - 1):
        x0, x1 = x_table[i], x_table[i + 1]
        y0, y1 = y_table[i], y_table[i + 1]
        if x0 <= x <= x1:
            # Perform linear interpolation
            return y0 + float(y1 - y0) * float(x - x0) / float(x1 - x0)

    # Shouldn't reach here if x is within range
    return None


# MQTT Settings
MQTT_BROKER = "192.168.1.109"  # Replace with your MQTT broker
MQTT_PORT = 1883
MQTT_TOPIC = "batteryPi"

# Initialize I2C and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 1  # Gain configuration; adjust for expected voltage range

# Create analog input channel (A0)
channel = AnalogIn(ads, ADS.P0)

# MQTT Client Setup
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

#Battery Voltage to Percent Interpolation:
percent= [0,    10,   20,    30,   40,   50,   60,   70,   80,   90,  99.99, 100]
levels = [40.0, 48.0, 51.2, 51.5, 52.0, 52.2, 52.3, 52.8, 53.1, 53.6, 54.4, 58.4]


# Main Loop
trimPot = 7996.0
R1 = (1.002*10**6) + (10.0*10**3)
R2 = (51.87*10**3) + trimPot

ratio = (R2 / (R1 + R2))

batteryVoltage = 0

try:
    while True:
        voltage = channel.voltage
        batteryVoltage = voltage / ratio
        print(f"Voltage: {batteryVoltage:.3f} V")

        batteryPercentage = interpolate(levels, percent, batteryVoltage)
        print(f"Battery Percentage: {batteryPercentage:.1f} %")

        message = { "battery_voltage": batteryVoltage, "battery_percent": batteryPercentage}
        client.publish(MQTT_TOPIC, json.dumps(message))
        time.sleep(15)  # Adjust frequency as needed
except KeyboardInterrupt:
    print("Exiting gracefully...")
    client.disconnect()
