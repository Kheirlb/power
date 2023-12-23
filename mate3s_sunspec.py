import sunspec2.modbus.client as client
import time

d = client.SunSpecModbusClientDeviceTCP(ipaddr="192.168.1.100", ipport=1025)
d.scan()

while True:
    print(time.time())
    print(f"Inverter Current: \t{d.inverter[0].A.value} \tAmps")
    print(f"Battery Voltage: \t{d.inverter[0].DCV.value / 10.0} \tVolts")
    print(f"Power Usage: \t\t{d.inverter[0].W.value} \tW")
    time.sleep(1)
