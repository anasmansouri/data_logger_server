from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers, status
from slaves_app.models import Setting,SensorValueType ,Slave
from .models import *


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('Baudrate', 'Parity', 'Stop', 'Bits')


class SensorValueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorValueType
        fields = ('Address', 'Name', 'Unit', 'value_class')



class SlaveSerializer(serializers.ModelSerializer):
    """
    A MachineSerializer serializer to return the student details
    """

    # user = UserSerializer(required=True)
    # main_pack = MainPackSerializer(required=True)

    class Meta:
        model = Slave
        fields = ('slave_address','setting', 'SensorValueType', 'name', 'enable', 'mac')

    def create(self, validated_data):
        try:
            slave_address = validated_data['slave_address']
            setting = validated_data["setting"]
            SensorValueType = validated_data["SensorValueType"]
            name = validated_data["name"]
            enable = validated_data["enable"]
            mac = validated_data["mac"]
        except KeyError:
            raise serializers.ValidationError({'error': "please make sure to fill all informations"})
        if setting == "" or SensorValueType == "" or name == "" or enable == "" or mac == "" or slave_address == "":
            raise serializers.ValidationError({'error': "please make sure to fill all informations"})
        if Slave.objects.filter(slave_address=validated_data["slave_address"]).exists():
            raise serializers.ValidationError({'error': 'there is a slave with the same address'})

        slave, created = Slave.objects.update_or_create(**validated_data)
        return slave
