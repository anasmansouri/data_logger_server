from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework import serializers


# Create your models here.


class Setting(models.Model):
    choices = (
        ('E', 'Even'), ('N', 'None'), ('O', 'Odd'), (0, 'default'))
    baud = (
        ('9600', '9600'), ('19200', '19200'), ('38400', '38400'))
    baudrate = models.CharField(max_length=10, choices=baud, blank=False)
    parity = models.CharField(max_length=5, choices=choices, blank=False)
    stopbits = models.PositiveSmallIntegerField(default=1)
    bytesize = models.PositiveSmallIntegerField(default=8)
    timeout = models.FloatField()

    def __str__(self):
        return self.baud


class Slave(models.Model):
    slave_address = models.IntegerField(primary_key=True, default=0,
                                        validators=[
                                            MaxValueValidator(247),
                                            MinValueValidator(0)
                                        ])
    setting = models.OneToOneField(Setting, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    enable = models.BooleanField(default=True)
    mac = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MemoryZone(models.Model):
    value_class_choices = (('FLOAT32', 'REAL (FLOAT32)'),
                           ('FLOAT32', 'SINGLE (FLOAT32)'),
                           ('FLOAT32', 'FLOAT32'),
                           ('UNIXTIMEF32', 'UNIXTIMEF32'),
                           ('FLOAT64', 'LREAL (FLOAT64)'),
                           ('FLOAT64', 'FLOAT  (FLOAT64)'),
                           ('FLOAT64', 'DOUBLE (FLOAT64)'),
                           ('FLOAT64', 'FLOAT64'),
                           ('UNIXTIMEF64', 'UNIXTIMEF64'),
                           ('INT64', 'INT64'),
                           ('UINT64', 'UINT64'),
                           ('UNIXTIMEI64', 'UNIXTIMEI64'),
                           ('UNIXTIMEI32', 'UNIXTIMEI32'),
                           ('INT32', 'INT32'),
                           ('UINT32', 'DWORD (UINT32)'),
                           ('UINT32', 'UINT32'),
                           ('INT16', 'INT (INT16)'),
                           ('INT16', 'INT16'),
                           ('UINT16', 'WORD (UINT16)'),
                           ('UINT16', 'UINT (UINT16)'),
                           ('UINT16', 'UINT16'),
                           ('BOOLEAN', 'BOOL (BOOLEAN)'),
                           ('BOOLEAN', 'BOOLEAN'),
                           ('STRING', 'STRING'),
                           )

    start_registers_address = models.CharField(max_length=50)
    name = models.CharField(max_length=200, blank=False)
    unit = models.CharField(max_length=50, blank=False)
    value_class = models.CharField(max_length=15, default='INT16', verbose_name="value_class",
                                   choices=value_class_choices)
    slave = models.ForeignKey(Slave, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name


class MemoryZoneHistory(models.Model):
    time_of_picking = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    memory_zone = models.ForeignKey(MemoryZone, on_delete=models.CASCADE)
    value = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return "value {} , data {}".format(self.time_of_picking, self.memory_zone)
