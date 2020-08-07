from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import transaction
from rest_framework import serializers, status
from slaves_app.models import Setting, MemoryZoneOfSlaves, Slave
from .models import *


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('baudrate', 'parity', 'stop', 'bits')


class MemoryZoneOfSlavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryZoneOfSlaves
        fields = ('start_registers_address', 'name', 'unit', 'value_class')


class SlaveSerializer(serializers.ModelSerializer):
    setting = SettingSerializer(required=True)
    MemoryZoneOfSlaves = MemoryZoneOfSlavesSerializer(many=True, write_only=True)

    class Meta:
        model = Slave
        fields = ('slave_address', 'setting',
                  'MemoryZoneOfSlaves',
                  'name', 'enable', 'mac')

    def create(self, validated_data):
        print(validated_data)
        for key in ["slave_address", 'setting',
                    'MemoryZoneOfSlaves',
                    'name', 'enable', 'mac']:
            if key not in validated_data:
                raise serializers.ValidationError({'error': "please make sure to fill the {}".format(key)})

        slave_address = validated_data['slave_address']
        setting_data = validated_data.pop("setting")
        MemoryZoneOfSlaves_list = validated_data.pop("MemoryZoneOfSlaves")
        name = validated_data["name"]
        enable = validated_data["enable"]
        mac = validated_data["mac"]

        setting = SettingSerializer.create(SettingSerializer(), validated_data=setting_data)
        slave, created = Slave.objects.update_or_create(setting=setting, **validated_data)
        slave.save()
        l = []
        for i in range(0, len(MemoryZoneOfSlaves_list)):
            slave.memoryzoneofslaves_set.create(
                start_registers_address=MemoryZoneOfSlaves_list[i]["start_registers_address"],
                name=MemoryZoneOfSlaves_list[i]["name"],
                unit=MemoryZoneOfSlaves_list[i]["unit"],
                value_class=MemoryZoneOfSlaves_list[i]["value_class"])
            print("start_registers_address {}\n".format(
                slave.memoryzoneofslaves_set.filter(name=MemoryZoneOfSlaves_list[i]["name"])
                    .first()))
            # solved
            # when we create the slave object the django use this serializer to return the json format to the client ,
            # but this give us an error , because the sensor value type is not an attribute for the slave model
            # how
            # using the write_only=True on the sensor value type field , so we are not allowing the serializer to look for the se
            # sensor value type to serialize it and add it to the json format of the slave .
        return slave


