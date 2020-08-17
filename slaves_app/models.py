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
    slave_address = models.IntegerField(primary_key=True,
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

    def get_memory_zones(self):
        return MemoryZone.objects.filter(slave=self)

    @staticmethod
    def get_enabled_slaves():
        return Slave.objects.filter(enable=True)


class MemoryZone(models.Model):
    id = models.AutoField(primary_key=True)
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
    slave = models.ForeignKey(Slave, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("slave", "start_registers_address"),)

    def __str__(self):
        return self.name

    def is_value_class_float_32(self):
        if self.value_class == "FLOAT32":
            return True
        else:
            return False

    def is_value_class_float_64(self):
        if self.value_class == "FLOAT64":
            return True
        else:
            return False

    def is_value_class_int_64(self):
        if self.value_class == "INT64":
            return True
        else:
            return False

    def is_value_class_uint_64(self):
        if self.value_class == "UINT64":
            return True
        else:
            return False

    def is_value_class_int_32(self):
        if self.value_class == "INT32":
            return True
        else:
            return False

    def is_value_class_uint_32(self):
        if self.value_class == "UINT":
            return True
        else:
            return False

    def is_value_class_int_16(self):
        if self.value_class == "INT16":
            return True
        else:
            return False

    def is_value_class_uint_16(self):
        if self.value_class == "UINT16":
            return True
        else:
            return False

    def is_value_class_string(self):
        if self.value_class == "STRING":
            return True
        else:
            return False

    def is_value_class_boolean(self):
        if self.value_class == "BOOLEAN":
            return True
        else:
            return False

    def read_value(self, slave_instrument):
        value = ""
        if self.is_value_class_float_32():
            value = slave_instrument.read_float(registeraddress=self.start_registers_address,
                                                functioncode=3,
                                                number_of_registers=2)
        elif self.is_value_class_float_64():
            value = slave_instrument.read_float(registeraddress=self.start_registers_address,
                                                functioncode=3,
                                                number_of_registers=4)
        # TODO maybe the problem is here
        elif self.is_value_class_int_64():
            # we can add an attribut named number_of_decimals in the memoryzone class
            # maybe we wil get an error because this function is private
            value = slave_instrument._generic_command(functioncode=3,
                                                      registeraddress=self.start_registers_address,
                                                      number_of_decimals=0,
                                                      number_of_registers=4,
                                                      signed=True,
                                                      )
        elif self.is_value_class_uint_64():
            # we can add an attribut named number_of_decimals in the memoryzone class
            value = slave_instrument._generic_command(functioncode=3,
                                                      registeraddress=self.start_registers_address,
                                                      number_of_decimals=0,
                                                      number_of_registers=4,
                                                      signed=False,
                                                      )

        elif self.is_value_class_int_32():
            # we can add an attribut named number_of_decimals in the memoryzone class
            value = slave_instrument.read_long(registeraddress=self.start_registers_address,
                                               functioncode=3, signed=True)
        elif self.is_value_class_uint_32():
            # we can add an attribut named number_of_decimals in the memoryzone class
            value = slave_instrument.read_long(registeraddress=self.start_registers_address,
                                               functioncode=3, signed=False)
        elif self.is_value_class_int_16():
            # we can add an attribut named number_of_decimals in the memoryzone class
            value = slave_instrument.read_register(registeraddress=self.start_registers_address,
                                                   functioncode=3, signed=True, number_of_decimals=0, )
        elif self.is_value_class_uint_16():
            # we can add an attribut named number_of_decimals in the memoryzone class
            value = slave_instrument.read_register(registeraddress=self.start_registers_address,
                                                   functioncode=3, signed=False, number_of_decimals=0, )
        elif self.is_value_class_string():
            # we can add an attribut named number_of_decimals in the memoryzone class
            value = slave_instrument.read_string(registeraddress=self.start_registers_address,
                                                 number_of_registers=16,
                                                 functioncode=3)
        elif self.is_value_class_boolean():
            # we can add an attribut named number_of_decimals in the memoryzone class
            value = slave_instrument.read_bit(registeraddress=self.start_registers_address, functioncode=2)
            # instead of printing we have to create a new history object and save it
        print(value)
        return value


class MemoryZoneHistory(models.Model):
    time_of_picking = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    memory_zone = models.ForeignKey(MemoryZone, on_delete=models.CASCADE)
    value = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return "value {} , data {}".format(self.time_of_picking, self.memory_zone)
