import requests

print("create a slave id : 2 ")
first_slave_data = {
    "slave_address": 1,
    "name": "power meter",
    "enable": True,
    "mac": "74-DE-AA-38-30-12",

    "setting": {
        "baudrate": 19200,
        "parity": "E",
        "stopbits": 1,
        "bytesize": 8,
        "timeout": 0.5
    }
}
x = requests.post(url='http://127.0.0.1:8000/slaves_app/Slaves/', json=first_slave_data)
print(x.json())

print("create a memory zone with id : 1 for slave  id : 1 ")
memory_zone_1_of_slave_1 = {
    "start_registers_address": 0,
    "name": "Voltage",
    "unit": "V",
    "type_of_value": "INT32",
    "number_of_decimals": 1,
    "slave": 1
}
x = requests.post(url='http://127.0.0.1:8000/slaves_app/MemoryZone/', json=memory_zone_1_of_slave_1)
print(x.json())

print("create a memory zone with id : 2 for slave  id : 1 ")
memory_zone_1_of_slave_1 = {
    "start_registers_address": 2,
    "name": "Amperage",
    "unit": "A",
    "type_of_value": "INT32",
    "number_of_decimals": 1,
    "slave": 1
}
x = requests.post(url='http://127.0.0.1:8000/slaves_app/MemoryZone/', json=memory_zone_1_of_slave_1)
print(x.json())

print("get all the slaves on the data base")

r = requests.get(url='http://127.0.0.1:8000/slaves_app/Slaves/')
print(r.json())

print("get all memory zones of  slave 1 ")

r = requests.get(url='http://127.0.0.1:8000/slaves_app/MemoryZone/')

for memory_zone in r.json():
    if memory_zone["slave"] == 1:
        print(memory_zone)
