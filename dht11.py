import machine
from time import sleep
from dht import DHT11
 
sensor = DHT11(machine.Pin(4))
 
while True:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    print(f'Temperature: {temp}, Humidity: {hum}')
    sleep(2)
