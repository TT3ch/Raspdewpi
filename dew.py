import time
import board
import busio
import adafruit_bme280
import RPi.GPIO as GPIO

# Initialize the BME280 sensors
i2c = busio.I2C(board.SCL, board.SDA)
bme1 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme2 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x77)

# Configure the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Set the dew point threshold value
dew_point_threshold = 15

while True:
    # Read the temperature and humidity values
    temperature1 = bme1.temperature
    humidity1 = bme1.relative_humidity
    
    temperature2 = bme2.temperature
    humidity2 = bme2.relative_humidity
    
    # Calculate the dew point
    dew_point1 = temperature1 - ((100 - humidity1)/5)
    dew_point2 = temperature2 - ((100 - humidity2)/5)
    
    # Check if the dew point reaches the threshold value
    if dew_point1 >= dew_point_threshold or dew_point2 >= dew_point_threshold:
        # Trigger the relay module
        GPIO.output(18, GPIO.HIGH)
    else:
        GPIO.output(18, GPIO.LOW)
    
    # Wait for 5 seconds
    time.sleep(5)
