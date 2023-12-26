import sunspec2.modbus.client as mate3s_client
import time
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Setup connection to mate3s
d = mate3s_client.SunSpecModbusClientDeviceTCP(ipaddr="192.168.1.100", ipport=1025)


# Setup connection to database
token = os.environ.get("INFLUXDB_TOKEN")
org = "Parks Ranch"
url = "http://192.168.1.108:8086"
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket="power"
write_api = write_client.write_api(write_options=SYNCHRONOUS)

while True:
    print(time.time())
    try:
        d.scan()
        inverter = d.inverter[0]
        inverter_current = inverter.A.value
        battery_voltage = inverter.DCV.value / 10.0
        power_usage = inverter.W.value
        print(f"Inverter Current: \t{inverter_current} \tAmps")
        print(f"Battery Voltage: \t{battery_voltage} \tVolts")
        print(f"Power Usage: \t\t{power_usage} \tW")
        point = (
            Point("mate3s")
            .field("Inverter Current", inverter_current)
            .field("Battery Voltage", battery_voltage)
            .field("Power Usage", power_usage)
        )
        write_api.write(bucket=bucket, org="Parks Ranch", record=point)
    except Exception as e:
        d = mate3s_client.SunSpecModbusClientDeviceTCP(ipaddr="192.168.1.100", ipport=1025)
        print(e)
    time.sleep(1)
