from machine import Pin
from time import sleep
from machine import Timer
from umqtt.simple import MQTTClient
import dht
import network
import time
import sys

sensor = dht.DHT11(Pin(4)) 
led = Pin('LED',Pin.OUT)

WIFI_SSID     = 'Tertiary infotech'
WIFI_PASSWORD = 'Tertiary888'

mqtt_client_id      = bytes('client_'+'123210', 'utf-8') # Just a random client ID

ADAFRUIT_IO_URL     = 'io.adafruit.com' 
ADAFRUIT_USERNAME   = 'XXXXXXXXXX'
ADAFRUIT_IO_KEY     = 'ZZZZZZZZZZZZZZZZZZZZ'

TEMP_FEED_ID      = 'temperature'
HUM_FEED_ID       = 'humidity'
TOGGLE_FEED_ID    = 'led'

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID,WIFI_PASSWORD)
    if not wifi.isconnected():
        print('Connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout < 5):
            print(5 - timeout)
            timeout = timeout + 1
            time.sleep(1) 
    if(wifi.isconnected()):
        print('Connected!')
    else:
        print('Not connected!')
        sys.exit()      

connect_wifi() # Connecting to WiFi Router 

client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
def connect_mqtt():
    try:
        print("Connecting to MQTT ...")
        client.connect()
    except Exception as e:
        print('Could not connect to MQTT server {}{}'.format(type(e).__name__, e))
        sys.exit()

connect_mqtt()
        
temp_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TEMP_FEED_ID), 'utf-8') # format - ~/feeds/temp
hum_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, HUM_FEED_ID), 'utf-8') # format - ~/feeds/hum
toggle_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID), 'utf-8') # format - ~/feeds/led

def sens_data(data):
    sensor.measure()                    # Measuring 
    temp = sensor.temperature()         # getting Temp
    hum = sensor.humidity()

    try:
        client.publish(temp_feed,    
                  bytes(str(temp), 'utf-8'),   # Publishing Temp feed to adafruit.io
                  qos=0)
    
        client.publish(hum_feed,    
                  bytes(str(hum), 'utf-8'),   # Publishing Hum feed to adafruit.io
                  qos=0)
    except:
        connect_mqtt()
        return

    if hum > 80:
        led.on()
    else:
        led.off()

    print("Temperature : ", str(temp))
    print("Humidity    : ", str(hum))
    print(' ')
    
timer = Timer(-1)
timer.init(period=10000, mode=Timer.PERIODIC, callback = sens_data)
