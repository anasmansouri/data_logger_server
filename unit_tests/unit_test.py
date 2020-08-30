import requests
import time

print("create a slave with id : 1 ")
first_slave_data = {
    "slave_address": 1,
    "name": "power meter",
    "enable": True,
    "mac": "AE-D9-F8-65-04-04",

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

print("create a slave with id : 2 ")
second_slave_data = {
    "slave_address": 2,
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
x = requests.post(url='http://127.0.0.1:8000/slaves_app/Slaves/', json=second_slave_data)
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
memory_zone_2_of_slave_1 = {
    "start_registers_address": 2,
    "name": "Amperage",
    "unit": "A",
    "type_of_value": "INT32",
    "number_of_decimals": 1,
    "slave": 1
}
x = requests.post(url='http://127.0.0.1:8000/slaves_app/MemoryZone/', json=memory_zone_1_of_slave_1)
print(x.json())

print("create a memory zone with id : 1 for slave  id : 2 ")
memory_zone_1_of_slave_2 = {
    "start_registers_address": 0,
    "name": "Voltage",
    "unit": "V",
    "type_of_value": "INT32",
    "number_of_decimals": 1,
    "slave": 2
}
x = requests.post(url='http://127.0.0.1:8000/slaves_app/MemoryZone/', json=memory_zone_1_of_slave_2)
print(x.json())

print("create a memory zone with id : 2 for slave  id : 2 ")
memory_zone_2_of_slave_2 = {
    "start_registers_address": 2,
    "name": "Amperage",
    "unit": "A",
    "type_of_value": "INT32",
    "number_of_decimals": 1,
    "slave": 2
}
x = requests.post(url='http://127.0.0.1:8000/slaves_app/MemoryZone/', json=memory_zone_2_of_slave_2)
print(x.json())

print("get all the slaves on the data base")
r = requests.get(url='http://127.0.0.1:8000/slaves_app/Slaves/')
print(r.json())

print("get all memory zones of  slave 1 ")
r = requests.get(url='http://127.0.0.1:8000/slaves_app/MemoryZone/')

for memory_zone in r.json():
    if memory_zone["slave"] == 1:
        print(memory_zone)

print("get all memory zones of  slave 2 ")
r = requests.get(url='http://127.0.0.1:8000/slaves_app/MemoryZone/')

for memory_zone in r.json():
    if memory_zone["slave"] == 2:
        print(memory_zone)

print("we have to wait for 30 seconds to give the celery server the time to read some data from the sensors and store "
      "them "
      "on the data base so we can read them ")
time.sleep(31)

slaves = requests.get(url='http://127.0.0.1:8000/slaves_app/Slaves/')
memory_zones_of_slaves = requests.get(url='http://127.0.0.1:8000/slaves_app/MemoryZone/')
memory_zones_data = requests.get(url='http://127.0.0.1:8000/slaves_app/MemoryZoneHistory/')

for slave in slaves.json():
    for memory_zone in memory_zones_of_slaves.json():
        if memory_zone["slave"] == slave["slave_address"]:
            for data in memory_zones_data.json():
                if memory_zone["id"] == data["memory_zone"]:
                    print("time of picking {} , value {}".format(data["time_of_picking"],
                                                                 data["value"]))
