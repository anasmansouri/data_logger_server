#!/usr/bin/env python3
import minimalmodbus
import serial
for i in range(0, 10):
	try:
		instrument = minimalmodbus.Instrument('/dev/ttyUSB0', i)
		instrument.serial.baudrate = 19200
		instrument.serial.bytesize = 8
		instrument.serial.parity   = serial.PARITY_EVEN
		instrument.serial.stopbits = 1
		instrument.serial.timeout  = 0.05                                                                                                       

		print(i)                                                                                                                                                       
		voltage_phase = instrument.read_long(registeraddress=0, functioncode=3)
		print("Read the Slave success !")
		print("voltage phase {}".format(voltage_phase))
		break
	except IOError:
    		print("Failed to read from instrument")