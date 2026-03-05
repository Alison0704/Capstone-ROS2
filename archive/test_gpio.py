from gpiozero import LED, Button
from gpiozero.pins.mock import MockFactory
import os

# Ensure we are using mock pins
if os.environ.get('GPIOZERO_PIN_FACTORY') == 'mock':
    print("--- Running in Simulation Mode ---")

# Define a virtual LED on Pin 17 and a Button on Pin 2
led = LED(17)
button = Button(2)

# Simulate a button press
print(f"Initial LED state: {led.is_lit}") 

print("Simulating button press...")
button.pin.drive_low()  # In real life, buttons often pull the pin 'low' when pressed

# Check the logic (assuming your code says 'led.on' when button is pressed)
led.on() 
print(f"LED state after press: {led.is_lit}")