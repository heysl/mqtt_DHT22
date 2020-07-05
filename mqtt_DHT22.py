import time
import logging

import Adafruit_DHT
import paho.mqtt.publish as publish

mqtt_host = "openhab.local"
mqtt_auth = {'username': "openhabian", 'password': None}

## set up logger:
# log to console
#logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# log to file
logging.basicConfig(filename='/home/pi/mqtt_DHT22/mqtt_DHT22.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.debug("Logger initialized")

## sensor foo
sensor = Adafruit_DHT.AM2302 
pin = 3
logging.debug("Sensor pin no. is {}".format(pin))

# try to get a sensor reading
h, t = Adafruit_DHT.read_retry(sensor, pin)
#h = None
#t = None
logging.debug("h is {}, t is {}".format(h, t))

# round sensor readings to neat little floats with one digit after point
if h is not None:
    humidity = round(h, 2)
else:
    humidity = None
if t is not None:
    temperature = round(t, 2)
else:
    temperature = None

logging.info("humidity is {}, temperature is {}".format(humidity, temperature))

## mqtt foo
# create mqtt-message
msgs = []
if humidity is not None:
    msg_h = {'topic': "terrarium/humidity", 'payload': "{}".format(humidity)}
    logging.debug("msg_h is {}".format(msg_h))
    msgs.append(msg_h)
    logging.debug("added {} to list 'msgs'".format(msg_h))
if temperature is not None:
    msg_t = {'topic': "terrarium/temperature", 'payload': "{}".format(temperature)}
    logging.debug("msg_t is {}".format(msg_t))
    msgs.append(msg_t)
    logging.debug("added {} to list 'msgs'".format(msg_t))

logging.debug("msgs-list: {}".format(msgs))

# now publish that stuff!
try:
    publish.multiple(msgs, hostname=mqtt_host, auth=mqtt_auth)
except Exception as e:
    logging.error("Exception while trying to publish to MQTT broker occured", exc_info=True)

