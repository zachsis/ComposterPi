import adafruit_max31855
from digitalio import DigitalInOut
import board
from prometheus_client import start_http_server, Gauge, Histogram
import time
import logging


#log = logging.getLogger('composter')
#log.setLevel(logging.INFO)


spi = board.SPI()
cs = DigitalInOut(board.D5)
sensor = adafruit_max31855.MAX31855(spi, cs)
t = Gauge('temperature', 'Current temperature in Ferenheit', ['scale'])

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32 

def get_temp():
    return celsius_to_fahrenheit(sensor.temperature)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(2323)
    # Generate some requests.
    while True:
        try:
            t.labels('C').set(sensor.temperature)
            t.labels('F').set(get_temp())
            print(get_temp())
            time.sleep(5)
        except:
            pass

