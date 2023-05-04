import time
import board
import busio
import adafruit_bme280
import RPi.GPIO as GPIO
import tkinter as tk

# Initialize the BME280 sensors
i2c = busio.I2C(board.SCL, board.SDA)
bme1 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme2 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x77)

# Configure the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Set the dew point threshold value
dew_point_threshold = 15

# Create a GUI interface
root = tk.Tk()
root.geometry("300x150")
root.title("Dew Point Calculator")

# Create a label for displaying the dew point value
dew_point_label = tk.Label(root, text="Dew Point: ")
dew_point_label.pack()

# Create a label for displaying the status of the relay module
status_label = tk.Label(root, text="Status: ")
status_label.pack()

# Create a button to turn on or off the relay module manually
def toggle_relay():
    if GPIO.input(18):
        GPIO.output(18, GPIO.LOW)
    else:
        GPIO.output(18, GPIO.HIGH)

button = tk.Button(root, text="Toggle Relay", command=toggle_relay)
button.pack()

def update_gui():
    # Read the temperature and humidity values
    temperature1 = bme1.temperature
    humidity1 = bme1.relative_humidity
    
    temperature2 = bme2.temperature
    humidity2 = bme2.relative_humidity
    
    # Calculate the dew point
    dew_point1 = temperature1 - ((100 - humidity1)/5)
    dew_point2 = temperature2 - ((100 - humidity2)/5)
    
    # Update the dew point label
    dew_point_label.config(text="Dew Point 1: {:.2f} °C\nDew Point 2: {:.2f} °C".format(dew_point1, dew_point2))
    
    # Check if dew point 1 is lower than dew point 2 and the dew point reaches the threshold value
    if dew_point1 < dew_point2 and (dew_point1 >= dew_point_threshold or dew_point2 >= dew_point_threshold):
        # Trigger the relay module
        GPIO.output(18, GPIO.HIGH)
        status_label.config(text="Status: Relay On")
    else:
        GPIO.output(18, GPIO.LOW)
        status_label.config(text="Status: Relay Off")
    
    # Wait for 5 seconds
    root.after(5000, update_gui)

# Start the GUI loop
update_gui()
root.mainloop()
