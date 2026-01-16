import sys
import sunspec2.modbus.client as mate3s_client

# Command line arguments
print('Usage: python3 mate3s-quick.py <inverterport> <pointName>')
if len(sys.argv) != 3:
    print("Error: Incorrect number of arguments.")
    sys.exit(1)
inverterport = int(sys.argv[1])
pointName = sys.argv[2]
ipaddr = "192.168.1.100"
tcpport = 1025
print(f"Connecting to Mate3S '{ipaddr}:{tcpport}', inverter '{inverterport}', point '{pointName}'...")

# Connect to Mate3S and read point.
d = mate3s_client.SunSpecModbusClientDeviceTCP(ipaddr=ipaddr, ipport=tcpport)
d.scan()
block = d.model_64115[inverterport]
print(block[pointName].cvalue)
