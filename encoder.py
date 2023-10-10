import RPi.GPIO as GPIO
import threading

class Encoder:
    def __init__(self, pin_a, pin_b):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.encoder_position = 0
        self.encoder_lock = threading.Lock()

        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Add event detection for the encoder
        GPIO.add_event_detect(self.pin_a, GPIO.FALLING, callback=self.encoder_callback, bouncetime=10)

    def encoder_callback(self, channel):
        with self.encoder_lock:
            state_a = GPIO.input(self.pin_a)
            state_b = GPIO.input(self.pin_b)

            if state_a == state_b:
                self.encoder_position += 1
            else:
                self.encoder_position -= 1

    def reset_encoder(self):
        with self.encoder_lock:
            self.encoder_position = 0

    def get_position(self):
        with self.encoder_lock:
            return self.encoder_position

    def cleanup(self):
        GPIO.cleanup()
