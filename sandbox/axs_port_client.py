from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("192.168.0.64", 5020)
# client.connect()
for i in  range(0, 65536):
  response = client.read_holding_registers(i)
  if (len(response.registers) > 0):
    print(f"{i}, {response.registers[0]}")
# response = client.read_holding_registers(40069 + 32)
# print(f"{response.registers}")
