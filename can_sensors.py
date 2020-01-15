import time
from lsm303d import LSM303D
from bmp280 import BMP280
import math
import os

try:
	from smbus2 import SMBus
except ImportError:
	from smbus import SMBus
	
texto_inicializando = "Inicializando "	
	
#Inicializar BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

#Inicializar acelerometro y magenetometro
lsm = LSM303D(0x1d)


#Inicializar valores de linea base para altitud
baseline_values = []
baseline_size = 100

print ("Recogiendo valores para linea base durante {:d} segundos. No mueva el sensor!\n".format(baseline_size))
for i in range(baseline_size):
	pressure = bmp280.get_pressure()
	baseline_values.append(pressure)
	texto_inicializando += "."
	print (texto_inicializando)
	time.sleep(0.2)
	os.system("clear")

baseline = sum(baseline_values[:-25]) / len(baseline_values[:-25])


while True:
	
	xyz = lsm.magnetometer()
	xyza = lsm.accelerometer()
	temperature = bmp280.get_temperature()
	pressure = bmp280.get_pressure()
	altitude = bmp280.get_altitude(qnh=baseline)
	
	print ("Temperatura: {:05.2f}*C -- Presion: {:05.2f}hPa".format(temperature, pressure))
	print ("Altitud relativa: {:05.2f} metros".format(altitude))
	print (("Magnetometro: {:+06.2f} : {:+06.2f} : {:+06.2f}").format(*xyz))
	print (("Acelerometro: {:+06.2f}g : {:+06.2f}g : {:+06.2f}g").format(*xyza))
	print ("\n")	
	time.sleep(0.1)
