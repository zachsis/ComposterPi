import adafruit_max31855
from digitalio import DigitalInOut
import board
from prometheus_client import start_http_server, Gauge, Histogram
import time
import logging
import yaml

# Read configuration from config.yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

temperature_offset = config['composterpy']['temperature-offset']
digital_io = getattr(board, config['composterpy']['digital-io'])
prometheus_interval = config['composterpy']['prometheus-interval']

# Initialize sensor
spi = board.SPI()
cs = DigitalInOut(digital_io)
sensor = adafruit_max31855.MAX31855(spi, cs)
t = Gauge('temperature', 'Current temperature in Fahrenheit', ['scale'])

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32 

def get_temp():
    readings = []
    for _ in range(100):
        readings.append(sensor.temperature)
        time.sleep(0.1)  # short delay between readings
    average_temp = sum(readings) / len(readings)
    calibrated_temp = average_temp + temperature_offset
    return celsius_to_fahrenheit(calibrated_temp)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(2323)
    # Generate some requests.
    while True:
        try:
            t.labels('C').set(sensor.temperature)
            t.labels('F').set(get_temp())
            print(get_temp())
            time.sleep(prometheus_interval)
        except Exception as E:
            print(E)
            pass


