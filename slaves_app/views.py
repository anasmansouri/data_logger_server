from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from slaves_app.models import Setting, MemoryZoneOfSlaves, Slave
from slaves_app.serializers import SettingSerializer, SlaveSerializer, MemoryZoneOfSlavesSerializer
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from rest_framework.filters import SearchFilter, OrderingFilter


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer


class MemoryZoneOfSlavesViewSet(viewsets.ModelViewSet):
    queryset = MemoryZoneOfSlaves.objects.all()
    serializer_class = MemoryZoneOfSlavesSerializer


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

    list_sensor_value_type = []
    for slave in queryset:
        list_sensor_value_type.append(list(MemoryZoneOfSlaves.objects.filter(slave=slave)))
    list_sensor_value_type_json = []
    for l in list_sensor_value_type:
        list_sensor_value_type_json.append(MemoryZoneOfSlavesSerializer(l, many=True))
    data = serializer.data
    for i in range(0, len(data)):
        data[i]["sensor_value_type"] = list_sensor_value_type_json[i].data
    return Response(data)

