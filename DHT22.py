import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22


def read_DHT(pin):
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, pin)
    return round(humidity, 3), round(temperature, 3)
