from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from slaves_app.models import  Setting ,SensorValueType,Slave
from slaves_app.serializers import SettingSerializer , SlaveSerializer ,  SensorValueTypeSerializer
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from rest_framework.filters import SearchFilter, OrderingFilter



#
#
# class SettingViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#
#     def create(self, request):
#         pass
#
#     @permission_classes([AllowAny ])
#     def list(self, request):
#         # search = request.GET.get('search', '')
#         queryset = list(Setting.objects.all())
#         #print(queryset)
#         # queryset.extend(list(MainPack.objects.filter(price__icontains=search)))
#         # queryset.extend(list(MainPack.objects.filter(exfiltermonth__icontains=search)))
#         # queryset.extend(list(MainPack.objects.filter(exfiltervolume__icontains=search)))
#         # queryset.extend(list(MainPack.objects.filter(packagedetail__icontains=search)))
#         # queryset = list(dict.fromkeys(queryset))
#         serializer = SettingSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = Setting.objects.all()
#         setting = get_object_or_404(queryset, pk=pk)
#         serializer = SettingSerializer(setting)
#         return Response(serializer.data)
#
#     @permission_classes([AllowAny])
#     def create(self, request):
#         # i catch those exception to be sure that the request contain the price and the exfilltermonth and the
#         # exfiltervolume
#         try:
#             Baudrate = request.data["Baudrate"],
#
#         except  KeyError:
#             raise serializers.ValidationError({'error': "please enter the Baudrate"})
#         try:
#             Parity = request.data["Parity"]
#         except  KeyError:
#             raise serializers.ValidationError({'error': "please enter the parity"})
#         try:
#             Stop = request.data["Stop"]
#         except  KeyError:
#             raise serializers.ValidationError({'error': "please enter the Stop bit"})
#         try:
#             Stop = request.data["Bits"]
#         except  KeyError:
#             raise serializers.ValidationError({'error': "please enter the Bits parameter"})
#
#         if Setting.objects.filter(
#                 Baudrate=request.data["Baudrate"],
#                 Parity=request.data["Parity"],
#                 Stop=request.data["Stop"],
#                 Bits=request.data["Bits"],
#         ).exists():
#             raise serializers.ValidationError(
#                 {'error': "there is already a setting object with the same parametres"})
#         setting = SettingSerializer.create(SettingSerializer(), validated_data=request.data)
#         return Response(SettingSerializer(setting).data)
#
#
#
#
#
# class SensorValueTypeViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#
#     def create(self, request):
#         pass
#
#     @permission_classes([AllowAny ])
#     def list(self, request):
#         # search = request.GET.get('search', '')
#         queryset = list(SensorValueType.objects.all())
#         #print(queryset)
#         # queryset.extend(list(MainPack.objects.filter(price__icontains=search)))
#         # queryset.extend(list(MainPack.objects.filter(exfiltermonth__icontains=search)))
#         # queryset.extend(list(MainPack.objects.filter(exfiltervolume__icontains=search)))
#         # queryset.extend(list(MainPack.objects.filter(packagedetail__icontains=search)))
#         # queryset = list(dict.fromkeys(queryset))
#         registers = SettingSerializer(queryset, many=True)
#         return Response(registers.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = SensorValueType.objects.all()
#         sensor_value_type = get_object_or_404(queryset, pk=pk)
#         serializer = SettingSerializer(sensor_value_type)
#         return Response(serializer.data)
#
#     @permission_classes([AllowAny])
#     def create(self, request):
#         # i catch those exception to be sure that the request contain the price and the exfilltermonth and the
#         # exfiltervolume
#         try:
#             Address = request.data["Address"],
#
#         except  KeyError:
#             raise serializers.ValidationError({'error': "please enter the register address"})
#         try:
#             Name = request.data["Name"]
#         except  KeyError:
#             raise serializers.ValidationError({'error': "please enter the register name "})
#         try:
#             Stop = request.data["Stop"]
#         except  KeyError:
#             raise serializers.ValidationError({'error': "please enter the Stop bit"})
#         try:
#             Stop = request.data["Bits"]
#         except  KeyError:
#             raise serializers.ValidationError({'error': "please enter the Bits parameter"})
#
#         if Setting.objects.filter(
#                 Baudrate=request.data["Baudrate"],
#                 Parity=request.data["Parity"],
#                 Stop=request.data["Stop"],
#                 Bits=request.data["Bits"],
#         ).exists():
#             raise serializers.ValidationError(
#                 {'error': "there is already a setting object with the same parametres"})
#         setting = SettingSerializer.create(SettingSerializer(), validated_data=request.data)
#         return Response(SettingSerializer(setting).data)
#
class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

class SensorValueTypeViewSet(viewsets.ModelViewSet):
    queryset = SensorValueType.objects.all()
    serializer_class = SensorValueTypeSerializer


class SlaveViewSet(viewsets.ModelViewSet):
    queryset = Slave.objects.all()
    serializer_class = SlaveSerializer


@api_view(['GET'])
@transaction.atomic
def salve_search(request):
    search = request.GET.get('search', '')
    queryset = list(Slave.objects.filter(name__icontains=search))
    queryset.extend(list(Slave.objects.filter(mac__icontains=search)))
    queryset.extend(list(Slave.objects.filter(slave_address__icontains=search)))
    queryset = list(dict.fromkeys(queryset))  # remounve deplicated items
    serializer = SlaveSerializer(queryset, many=True)
    return Response(serializer.data)