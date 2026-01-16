"""Main power room python service (mate3s to mqtt)."""
import time
import datetime
import config
import mate3s_sunspec
import json
import paho.mqtt.client as mqtt

# Setup inverter connection.
inverters = mate3s_sunspec.connect()

# MQTT Settings and Setup
MQTT_BROKER = config.hostname
MQTT_INVERTER1_TOPIC = "ranch/power/inverter/01/telemetry"
MQTT_INVERTER2_TOPIC = "ranch/power/inverter/02/telemetry"
MQTT_INVERTER3_TOPIC = "ranch/power/inverter/03/telemetry"
MQTT_TOTALS_TOPIC =    "ranch/power/inverter/totals/telemetry"
MQTT_PORT = 1883
client = mqtt.Client()
result = client.connect(MQTT_BROKER, MQTT_PORT, 60)
print("MQTT connect result: ", result)

while True:
    print(datetime.datetime.now())

    try:
        # Get data from inverters.
        messages = mate3s_sunspec.get_mqtt_data(inverters)

        # Publish data to MQTT.
        client.publish(MQTT_TOTALS_TOPIC, json.dumps(messages[0]))
        client.publish(MQTT_INVERTER1_TOPIC, json.dumps(messages[1]))
        client.publish(MQTT_INVERTER2_TOPIC, json.dumps(messages[2]))
        client.publish(MQTT_INVERTER3_TOPIC, json.dumps(messages[3]))

    except Exception as e:
        print(e)
        # TODO(kparks) Restart all connections?

    # Do a sleep loop.
    time.sleep(config.delay_s)
