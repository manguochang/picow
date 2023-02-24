from machine import Pin
from time import sleep
from machine import Timer
from umqtt.simple import MQTTClient
import dht
import network
import time
import sys

led = Pin("LED",Pin.OUT)

WIFI_SSID     = 'Tertiary infotech'
WIFI_PASSWORD = 'Tertiary888'

mqtt_client_id      = bytes('client_'+'123210', 'utf-8') # Just a random client ID

ADAFRUIT_IO_URL     = 'io.adafruit.com' 
ADAFRUIT_USERNAME   = 'XXXXXXXXXX'
ADAFRUIT_IO_KEY     = 'ZZZZZZZZZZZZZZZZZZZZ'

TOGGLE_FEED_ID      = 'led'

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


def cb(topic, msg): # callback function
    print('Received Data: Topic = {}, Msg = {}'.format(topic, msg))
    received_data = str(msg, 'utf-8') # Receiving data 
    if received_data == "ON":
        print("on")
        led.on()
    if received_data == "OFF":
        print("off")
        led.off()
        
toggle_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID), 'utf-8') # format - ~/feeds/led

client.set_callback(cb) # callback function
client.subscribe(toggle_feed) # subscribing to particular topic
    
while True:
    try:
        client.check_msg() # non blocking function
    except:
        client.disconnect()
        print("Error")
        sys.exit()

