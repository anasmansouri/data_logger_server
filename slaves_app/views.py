from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from slaves_app.models import Setting, MemoryZone, Slave, MemoryZoneHistory
from slaves_app.serializers import SettingSerializer, SlaveSerializer, MemoryZoneSerializer, MemoryZoneHistorySerializer
from . import my_own_lib
from .functions import \
    get_slaves_the_client_is_looking_for, convert_list_of_slaves_to_json_format, \
    link_memory_zones_with_their_slave_in_a_json_format, get_all_memory_zones_for_each_slave_in_json_format


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer


class MemoryZoneViewSet(viewsets.ModelViewSet):
    queryset = MemoryZone.objects.all()
    serializer_class = MemoryZoneSerializer


# Todo  we have to allow only the get

class MemoryZoneHistoryViewSet(viewsets.ModelViewSet):
    queryset = MemoryZoneHistory.objects.all()
    serializer_class = MemoryZoneHistorySerializer


class SlaveViewSet(viewsets.ModelViewSet):
    queryset = Slave.objects.all()
    serializer_class = SlaveSerializer


@api_view(['GET'])
@transaction.atomic
def look_for_slaves(request):
    slaves = get_slaves_the_client_is_looking_for(request)
    memory_zones_json = get_all_memory_zones_for_each_slave_in_json_format(slaves)
    slaves_in_json = convert_list_of_slaves_to_json_format(slaves)
    slaves_in_json = link_memory_zones_with_their_slave_in_a_json_format(slaves_in_json,
                                                                         memory_zones_json)
    return Response(slaves_in_json)
