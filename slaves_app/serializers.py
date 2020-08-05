from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import transaction
from rest_framework import serializers, status
from slaves_app.models import Setting,Sensor_value_type ,Slave
from .models import *


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('baudrate', 'parity', 'stop', 'bits')


class SensorValueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor_value_type
        fields = ('start_registers_address', 'name', 'unit', 'value_class')



class SlaveSerializer(serializers.ModelSerializer):
    setting = SettingSerializer(required=True)
    sensor_value_type = SensorValueTypeSerializer(required=True,many=True)
    class Meta:
        model = Slave
        fields = ('slave_address','setting',
                  'sensor_value_type',
                  'name', 'enable', 'mac')


    def create(self, validated_data):
        try:
            slave_address = validated_data['slave_address']
            setting_data = validated_data.pop("setting")
            SensorValueType_list = validated_data.pop("sensor_value_type")

            name = validated_data["name"]
            enable = validated_data["enable"]
            mac = validated_data["mac"]
        except KeyError:
            raise serializers.ValidationError({'error': "please make sure to fill all informations"})

        setting = SettingSerializer.create(SettingSerializer(),validated_data=setting_data)
        slave, created = Slave.objects.update_or_create(setting=setting, **validated_data)
        slave.save()
        l=[]
        for i in range(0,len(SensorValueType_list)):
            #s =SensorValueType.objects.create(start_registers_address=SensorValueType_list[i]["start_registers_address"],
            #                               name=SensorValueType_list[i]["name"],
            #                               unit=SensorValueType_list[i]["unit"],
            #                               value_class=SensorValueType_list[i]["value_class"])
            #s.save()
            #l.append(s)
            slave.sensor_value_type_set.create(start_registers_address=SensorValueType_list[i]["start_registers_address"],
                                          name=SensorValueType_list[i]["name"],
                                           unit=SensorValueType_list[i]["unit"],
                                           value_class=SensorValueType_list[i]["value_class"])
            print("start_registers_address {}\n".format(slave.sensor_value_type_set.filter(name=SensorValueType_list[i]["name"])
                                                        .first()))
            #slave.save()
        # if setting == "" or SensorValueType == "" or name == "" or enable == "" or mac == "" or slave_address == "":
        #    raise serializers.ValidationError({'error': "please make sure to fill all informations"})
        # if Slave.objects.get(slave_address=validated_data["slave_address"]).exists():
        #     raise serializers.ValidationError({'error': 'there is a slave with the same address'})

        return slave
