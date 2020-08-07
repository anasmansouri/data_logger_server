from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from slaves_app.models import Setting, MemoryZone, Slave, MemoryZoneHistory
from slaves_app.serializers import SettingSerializer, SlaveSerializer, MemoryZoneSerializer, MemoryZoneHistorySerializer
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from rest_framework.filters import SearchFilter, OrderingFilter

## minimalmodbus

import minimalmodbus


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer


class MemoryZoneViewSet(viewsets.ModelViewSet):
    queryset = MemoryZone.objects.all()
    serializer_class = MemoryZoneSerializer


# we have to allow only the get

class MemoryZoneHistoryViewSet(viewsets.ModelViewSet):
    queryset = MemoryZoneHistory.objects.all()
    serializer_class = MemoryZoneHistorySerializer


class SlaveViewSet(viewsets.ModelViewSet):
    queryset = Slave.objects.all()
    serializer_class = SlaveSerializer


# to serach items using the name or the mac address or the slave address .
# the return type is list of slaves in json format
@api_view(['GET'])
@transaction.atomic
def salve_search(request):
    search = request.GET.get('search', '')
    queryset = list(Slave.objects.filter(name__startswith=search))
    queryset.extend(list(Slave.objects.filter(mac__startswith=search)))
    queryset.extend(list(Slave.objects.filter(slave_address__startswith=search)))
    # remounve deplicated items
    queryset = list(dict.fromkeys(queryset))
    serializer = SlaveSerializer(queryset, many=True)

    list_memory_zone = []
    for slave in queryset:
        list_memory_zone.append(list(MemoryZone.objects.filter(slave=slave)))
    list_memory_zone_json = []
    for l in list_memory_zone:
        list_memory_zone_json.append(MemoryZoneSerializer(l, many=True))
    data = serializer.data
    for i in range(0, len(data)):
        data[i]["memory_zone"] = list_memory_zone_json[i].data
    return Response(data)


######################################

@api_view(["GET"])
@transaction.atomic
def read_data(request):
    Instruments = []
    enabled_slaves = Slave.objects.filter(enable=True)

    for slave in enabled_slaves:
        instrument = minimalmodbus.Instrument('/dev/ttyUSB0', slave.slave_address)
        instrument.serial.baudrate = slave.setting.baudrate
        instrument.serial.parity = slave.setting.parity
        instrument.serial.stopbits = slave.setting.bits
        instrument.serial.bytesize = slave.setting.bytesize
        instrument.serial.timeout = slave.setting.timeout
        instrument.mode = minimalmodbus.MODE_RTU
        Instruments.append(instrument)
    for i in range(0, len(enabled_slaves)):
        # we can improve it later using slave.memoryzone_set
        MemoryZones = MemoryZone.objects.filter(slave=enabled_slaves[i])
        for memoryzone in MemoryZones:
            type = memoryzone.value_class
            if type == "FLOAT32":
                value = Instruments[i].read_float(registeraddress=memoryzone.start_registers_address,
                                                  functioncode=3,
                                                  number_of_registers=2)
            elif type == "FLOAT64":
                value = Instruments[i].read_float(registeraddress=memoryzone.start_registers_address,
                                                  functioncode=3,
                                                  number_of_registers=4)
            elif type == "INT64":
                # we can add an attribut named number_of_decimals in the memoryzone class
                # maybe we wil get an error because this function is private
                value = Instruments[i]._generic_command(functioncode=3,
                                                        registeraddress=memoryzone.start_registers_address,
                                                        number_of_decimals=0,
                                                        number_of_registers=4,
                                                        signed=True,
                                                        )
            elif type == "UINT64":
                # we can add an attribut named number_of_decimals in the memoryzone class
                value = Instruments[i]._generic_command(functioncode=3,
                                                        registeraddress=memoryzone.start_registers_address,
                                                        number_of_decimals=0,
                                                        number_of_registers=4,
                                                        signed=False,
                                                        )

            elif type == "INT32":
                # we can add an attribut named number_of_decimals in the memoryzone class
                value = Instruments[i].read_long(registeraddress=memoryzone.start_registers_address,
                                                 functioncode=3, signed=True)
            elif type == "UINT32":
                # we can add an attribut named number_of_decimals in the memoryzone class
                value = Instruments[i].read_long(registeraddress=memoryzone.start_registers_address,
                                                 functioncode=3, signed=False)
            elif type == "INT16":
                # we can add an attribut named number_of_decimals in the memoryzone class
                value = Instruments[i].read_register(registeraddress=memoryzone.start_registers_address,
                                                     functioncode=3, signed=True, number_of_decimals=0, )
            elif type == "UINT16":
                # we can add an attribut named number_of_decimals in the memoryzone class
                value = Instruments[i].read_register(registeraddress=memoryzone.start_registers_address,
                                                     functioncode=3, signed=False, number_of_decimals=0, )
            elif type == "STRING":
                # we can add an attribut named number_of_decimals in the memoryzone class
                value = Instruments[i].read_string(registeraddress=memoryzone.start_registers_address,
                                                   number_of_registers=16,
                                                   functioncode=3)
            elif type == "BOOLEAN":
                # we can add an attribut named number_of_decimals in the memoryzone class
                value = Instruments[i].read_bit(registeraddress=memoryzone.start_registers_address, functioncode=2)
            # instead of printing we have to create a new history object and save it
            print(value)
