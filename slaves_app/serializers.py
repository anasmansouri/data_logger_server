from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import transaction
from rest_framework import serializers, status
from slaves_app.models import Setting, MemoryZone, Slave
from .models import *


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('baudrate', 'parity', 'stopbits', 'bytesize', 'timeout')


class MemoryZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryZone
        fields = ('start_registers_address', 'name', 'unit', 'value_class')


class MemoryZoneHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryZoneHistory
        fields = ('time_of_picking', 'memory_zone', 'value')


class SlaveSerializer(serializers.ModelSerializer):
    setting = SettingSerializer(required=True)
    MemoryZone = MemoryZoneSerializer(many=True, write_only=True)

    class Meta:
        model = Slave
        fields = ('slave_address', 'setting',
                  'MemoryZone',
                  'name', 'enable', 'mac')

    def create(self, validated_data):
        print(validated_data)
        for key in ["slave_address", 'setting',
                    'MemoryZone',
                    'name', 'enable', 'mac']:
            if key not in validated_data:
                raise serializers.ValidationError({'error': "please make sure to fill the {}".format(key)})

        slave_address = validated_data['slave_address']
        setting_data = validated_data.pop("setting")
        MemoryZone_list = validated_data.pop("MemoryZone")
        name = validated_data["name"]
        enable = validated_data["enable"]
        mac = validated_data["mac"]

        setting = SettingSerializer.create(SettingSerializer(), validated_data=setting_data)
        slave, created = Slave.objects.update_or_create(setting=setting, **validated_data)
        slave.save()
        l = []
        for i in range(0, len(MemoryZone_list)):
            slave.memoryzone_set.create(
                start_registers_address=MemoryZone_list[i]["start_registers_address"],
                name=MemoryZone_list[i]["name"],
                unit=MemoryZone_list[i]["unit"],
                value_class=MemoryZone_list[i]["value_class"])
            print("start_registers_address {}\n".format(
                slave.memoryzone_set.filter(name=MemoryZone_list[i]["name"])
                    .first()))
            # solved
            # when we create the slave object the django use this serializer to return the json format to the client ,
            # but this give us an error , because the sensor value type is not an attribute for the slave model
            # how
            # using the write_only=True on the sensor value type field , so we are not allowing the serializer to look for the se
            # sensor value type to serialize it and add it to the json format of the slave .
        return slave
