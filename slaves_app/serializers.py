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
        fields = ('id', 'slave', 'start_registers_address', 'name', 'unit', 'type_of_value', 'number_of_decimals')
        extra_kwargs = {
            'id': {'required': False, 'read_only': True}
        }


class MemoryZoneHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryZoneHistory
        fields = ('time_of_picking', 'memory_zone', 'value')


class SlaveSerializer(serializers.ModelSerializer):
    setting = SettingSerializer(required=True)

    class Meta:
        model = Slave
        fields = ('slave_address', 'setting',
                  'name', 'enable', 'mac')

    def create(self, validated_data):
        print(validated_data)
        for key in ["slave_address", 'setting',
                    'name', 'enable', 'mac']:
            if key not in validated_data:
                raise serializers.ValidationError({'error': "please make sure to fill the {}".format(key)})

        slave_address = validated_data['slave_address']
        setting_data = validated_data.pop("setting")
        name = validated_data["name"]
        enable = validated_data["enable"]
        mac = validated_data["mac"]

        setting = SettingSerializer.create(SettingSerializer(), validated_data=setting_data)
        slave, created = Slave.objects.update_or_create(setting=setting, **validated_data)
        slave.save()

        # solved when we create the slave object the django use this serializer to return the json format to the
        # client , but this give us an error , because the sensor value type is not an attribute for the slave model
        # how using the write_only=True on the sensor value type field , so we are not allowing the serializer to
        # look for the se sensor value type to serialize it and add it to the json format of the slave .
        return slave
