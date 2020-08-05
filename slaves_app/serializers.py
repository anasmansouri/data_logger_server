from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers, status
from slaves_app.models import Setting,SensorValueType ,Slave
from .models import *


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('baudrate', 'parity', 'stop', 'bits')


class SensorValueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorValueType
        fields = ('start_registers_address', 'name', 'unit', 'value_class')



class SlaveSerializer(serializers.ModelSerializer):
    setting = SettingSerializer()
    sensor_value_type = SensorValueTypeSerializer(many=True)
    class Meta:
        model = Slave
        fields = ('slave_address','setting', 'sensor_value_type', 'name', 'enable', 'mac')

    def create(self, validated_data):
        try:
            slave_address = validated_data['slave_address']
            setting = validated_data["setting"]
            SensorValueType = validated_data["sensor_value_type"]
            name = validated_data["name"]
            enable = validated_data["enable"]
            mac = validated_data["mac"]
            print('hadi f5ater l5water')
        except KeyError:
            raise serializers.ValidationError({'error': "please make sure to fill all informations"})
        # if setting == "" or SensorValueType == "" or name == "" or enable == "" or mac == "" or slave_address == "":
        #    raise serializers.ValidationError({'error': "please make sure to fill all informations"})
        # if Slave.objects.get(slave_address=validated_data["slave_address"]).exists():
        #     raise serializers.ValidationError({'error': 'there is a slave with the same address'})
        print("validated data {}".format(validated_data))
        slave, created = Slave.objects.update_or_create(**validated_data)
        print('rah creyina slave ')
        return slave
