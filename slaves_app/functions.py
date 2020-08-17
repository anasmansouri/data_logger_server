import minimalmodbus
from slaves_app.models import Slave


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
    instrument.serial.stopbits = slave.setting.bits
    instrument.serial.bytesize = slave.setting.bytesize
    instrument.serial.timeout = slave.setting.timeout
    instrument.mode = minimalmodbus.MODE_RTU
    return instrument


