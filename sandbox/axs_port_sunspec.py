# import ipaddress
import sunspec2.modbus.client as client

# Creating the connection.
# A static ip address is set for the AXS unit at 192.168.0.64 using the config file on the SD card.
# Using port 5020 instead of 502 to avoid firewall issues.
d = client.SunSpecModbusClientDeviceTCP(ipaddr="192.168.1.100", ipport=1025)

# Scan for the available models. In my test case, there will only be the 64110 OutBack block since nothing else is connected to the AXS Port.
d.scan()

# One of the values I can extract is the reported tcp ip address value.
# ip = d.model_64110[0].TCPIP_address.value
# print("ip address read from the AXS port:", ipaddress.ip_address(ip))

if "model_64110" in d.models:
  print("model_64110", d.model_64110[0])

if "model_64115" in d.models:
  print("model_64115", d.model_64115[0])
else:
  print("sadly, did not find 64115")

if "inverter" in d.models:
  print(d.inverter[0])
  
inverter_1 = d.model_64115[0]
inverter_2 = d.model_64115[1]
inverter_3 = d.model_64115[2]
print(f"Inverter 1: \t{inverter_1.GS_Split_Load_kW.value} kW")
print(f"Inverter 2: \t{inverter_2.GS_Split_Load_kW.value} kW")
print(f"Inverter 3: \t{inverter_3.GS_Split_Load_kW.value} kW")
print(f"Inverter 1: \t{inverter_1.GS_Split_Load_kW.cvalue} kW")
print(f"Inverter 2: \t{inverter_2.GS_Split_Load_kW.cvalue} kW")
print(f"Inverter 3: \t{inverter_3.GS_Split_Load_kW.cvalue} kW")


print(f"Inverters: \t{d.inverter[0].W.value} W")
