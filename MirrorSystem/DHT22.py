#!/usr/bin/env python
import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 18

def getNowTemp() :
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if temperature is not None :
		return '{0:0.1f}*C%'.format(temperature)
	else:
		return 'Error'
