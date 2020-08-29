import minimalmodbus

from slaves_app import my_own_lib
from slaves_app.models import Slave
from slaves_app.serializers import MemoryZoneSerializer, SlaveSerializer


def read_sensors_values(slaves):
    for slave in slaves:
        read_memory_zones(slave)


def read_memory_zones(slave):
    slave_instrument = create_slave_instrument(slave)
    slave_memory_zones = slave.get_memory_zones()
    [print(memory_zone.read_value(slave_instrument)) for memory_zone in slave_memory_zones]


def create_slave_instrument(slave):
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', slave.slave_address)
    instrument.serial.baudrate = slave.setting.baudrate
    instrument.serial.parity = slave.setting.parity
    instrument.serial.stopbits = slave.setting.stopbits
    instrument.serial.bytesize = slave.setting.bytesize
    instrument.serial.timeout = slave.setting.timeout
    instrument.mode = minimalmodbus.MODE_RTU
    return instrument


def get_slaves_the_client_is_looking_for(request):
    keyword = request.GET.get('search', '')
    slaves_with_redundancy = Slave.get_slaves_with_name_or_mac_or_address_start_with(keyword=keyword)
    slaves = my_own_lib.remove_redundancy_items_from_the_list(queryset=slaves_with_redundancy)
    return slaves


def get_all_memory_zones_for_each_slave_in_json_format(slaves):
    memory_zones = []
    for slave in slaves:
        memory_zones.append(MemoryZoneSerializer(list(slave.get_memory_zones()), many=True))
    return memory_zones


def convert_list_of_slaves_to_json_format(slaves):
    slaves_serialized = SlaveSerializer(slaves, many=True)
    slaves_in_json = slaves_serialized.data
    return slaves_in_json


def link_memory_zones_with_their_slave_in_a_json_format(slaves_in_json, memory_zones_json):
    for i in range(0, len(slaves_in_json)):
        slaves_in_json[i]["memory_zone"] = memory_zones_json[i].data
    return slaves_in_json
