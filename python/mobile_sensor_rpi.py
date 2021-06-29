#%%
import sys
print(sys.version)
import board
import busio
from digitalio import DigitalInOut, Direction
import serial
import json
import datetime
import time
import adafruit_bme280
import math

#%%
def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

try:
    import struct
except ImportError:
    import ustruct as struct
 
 
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT
 
# Connect to BME280 sensors using I2C
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
# Connect to PMS5003 sensor using the serial port
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
buffer = []
 
# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25

# open a unique file to store sensor data
fn = '/home/pi/SpokaneSchools/Data/aqSensorData_' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.csv'
f  = open(fn,'w')
f.write('Time,Temperature,RelativeHumidity,Pressure,PM25\n');

while True:
    Time = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')

    # Read data from the PMS5003 sensor and parse the data
    data = uart.read(32)  # read up to 32 bytes
    data = list(data)
    print("read: ", data)          # this is a bytearray type
 
    buffer += data
    while buffer and buffer[0] != 0x42:
        buffer.pop(0)
 
    if len(buffer) > 200:
        buffer = []  # avoid an overrun if all bad data
    if len(buffer) < 32:
        continue
 
    if buffer[1] != 0x4d:
        buffer.pop(0)
        continue
 
    frame_len = struct.unpack(">H", bytes(buffer[2:4]))[0]
    if frame_len != 28:
        buffer = []
        continue
 
    frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:]))

    pm10_standard, pm25_standard, pm100_standard, pm10_env, \
        pm25_env, pm100_env, particles_03um, particles_05um, particles_10um, \
        particles_25um, particles_50um, particles_100um, skip, checksum = frame
 
    check = sum(buffer[0:30])
 
    if check != checksum:
        buffer = []
        continue

    # Save data to the file.
    f.write(Time + ',' + str(bme280.temperature) + ',' +  str(bme280.humidity) + ',' +  str(bme280.pressure) + ',' +  str(pm25_env) + '\n');
    f.close()

    # Print the data to screen
    date_time = datetime.datetime.now()
    print(date_time)

    print("\nTemperature: %0.1f C" % bme280.temperature)
    print("Humidity: %0.1f %%" % bme280.humidity)
    print("Pressure: %0.1f hPa" % bme280.pressure)
    print("Altitude = %0.2f meters" % bme280.altitude)

    print("Concentration Units (standard)")
    print("---------------------------------------")
    print("PM 1.0: %d\tPM2.5: %d\tPM10: %d" % (pm10_standard, pm25_standard, pm100_standard))
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print("PM 1.0: %d\tPM2.5: %d\tPM10: %d" % (pm10_env, pm25_env, pm100_env))
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", particles_03um)
    print("Particles > 0.5um / 0.1L air:", particles_05um)
    print("Particles > 1.0um / 0.1L air:", particles_10um)
    print("Particles > 2.5um / 0.1L air:", particles_25um)
    print("Particles > 5.0um / 0.1L air:", particles_50um)
    print("Particles > 10 um / 0.1L air:", particles_100um)
    print("---------------------------------------")

    time.sleep(10) # delay ten seconds 
    buffer = buffer[32:]
    f = open(fn, 'a')

