import RPi.GPIO as GPIO
import threading
import time

# Define GPIO pins for the encoder
PIN_A = 17  # Replace with your actual GPIO pin numbers
PIN_B = 18

# Global variables for encoder position
encoder_position = 0
encoder_lock = threading.Lock()

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to update encoder position
def encoder_callback(channel):
    global encoder_position
    global encoder_lock

    with encoder_lock:
        state_A = GPIO.input(PIN_A)
        state_B = GPIO.input(PIN_B)

        if state_A == state_B:
            encoder_position += 1
        else:
            encoder_position -= 1

# Thread for encoder tracking
def encoder_thread():
    GPIO.add_event_detect(PIN_A, GPIO.FALLING, callback=encoder_callback, bouncetime=10)

# Your main code
def main_code():
    while True:
        # Your main code here
        print(f"Encoder position: {encoder_position}")
        time.sleep(1)

if __name__ == "__main__":
    try:
        encoder_thread = threading.Thread(target=encoder_thread)
        encoder_thread.daemon = True  # Set as daemon to exit when the main program exits
        encoder_thread.start()

        main_code()

    except KeyboardInterrupt:
        pass

    finally:
        GPIO.cleanup()  # Cleanup GPIO on program exit
