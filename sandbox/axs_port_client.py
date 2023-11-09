import struct
from pymodbus.client import ModbusTcpClient
import csv

rows = [None] * 66536

with open('non_empty_axs_registers.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    # extracting each data row one by one
    for row in csvreader:
        addr = int(row[0])
        value = int(row[1])
        rows[addr] = value

# with open()

SUNSPEC_START_REG = 40000 # 0, 50000 are also legal.
SUNS_END_MODEL_ID = 0xffff

# client = ModbusTcpClient("192.168.0.64", 5020)
# client.connect()
# for i in  range(0, 65536):
#   response = client.read_holding_registers(i)
#   if (len(response.registers) > 0):
#     print(f"{i}, {response.registers[0]}")
# response = client.read_holding_registers(40069 + 32)
# print(f"{response.registers}")

def data_to_u16(data):
    u16 = struct.unpack('>H', data[:2])
    return u16[0]

class PowerRoomClient:
    def __init__(self, ip_address="192.168.0.64", port=5020) -> None:
        self.base_addr = SUNSPEC_START_REG
        # self.client = ModbusTcpClient(ip_address, port)

    # def read(self, address=SUNSPEC_START_REG, count=1):
    #     response = self.client.read_holding_registers(address, count)
    #     return response.registers

    def read(self, address=SUNSPEC_START_REG, count=1):
        data_blob = []
        for addr in range(address, address+count):
            data_blob.append(rows[addr])
        return data_blob

    def read_common_block(self):
        marker = self.read(count=2)
        return self.read_block(self.base_addr + 2)

    def read_block(self, start_addr):
        print("start_addr:", start_addr)
        did = self.read(start_addr, 1)[0]
        L = self.read(start_addr + 1, 1)[0]
        block = self.read(start_addr + 2, L)
        print("did:", did)
        print("length:", L)
        print(block)
        return did, start_addr + 2 + L

    def scan(self):
        did, next_addr = self.read_common_block()
        print("\nSearching for next block...")
        search = True
        while search:
            did, next_addr = self.read_block(next_addr)
            if did == 0xFFFF:
                print("Found end model did 0xFFFF")
                search = False
            elif did == 0:
                print("Invalid, did == 0")
                search = False
            else:
                print("\nSearching next block...")

# import sunspec2.modbus.client as client
# d = client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='192.168.0.64', ipport=5020)
# d.scan() # this fails...

client = PowerRoomClient()
# print(client.read(count=4))
# client.read_common_block()
client.scan()
# client.read_block(40069)