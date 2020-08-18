from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny

from slaves_app.functions import read_sensors_values
from slaves_app.models import Setting, MemoryZone, Slave, MemoryZoneHistory
from slaves_app.serializers import SettingSerializer, SlaveSerializer, MemoryZoneSerializer, MemoryZoneHistorySerializer
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from . import my_one_lib

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
# TODO you have to try to remove the slave attributes in the json return of this function
@api_view(['GET'])
@transaction.atomic
def salve_search(request):
    keyword = request.GET.get('search', '')
    queryset = Slave.get_slaves_with_name_or_mac_or_address_start_with(keyword=keyword)
    queryset = my_one_lib.remove_redundancy_items_from_a_list(queryset=queryset)
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
    enabled_slaves = Slave.get_enabled_slaves()
    read_sensors_values(enabled_slaves)
    return Response({"data", "koulchi naadi"})
