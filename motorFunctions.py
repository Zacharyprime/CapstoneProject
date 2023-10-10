import RPi.GPIO as GPIO
class Motor:
    def __init__(self, pwm_pin, control_pin_a, control_pin_b):
        self.pwmPin = pwm_pin
        self.CONTROL_PIN_A = control_pin_a
        self.CONTROL_PIN_B = control_pin_b

    def set_pwm(self, duty_cycle):
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwmPin, GPIO.OUT)

        # Create PWM object
        pwm = GPIO.PWM(self.pwmPin, 1000)  # 1 kHz frequency
        pwm.start(duty_cycle)  # Start with the specified duty cycle

    def set_channel(self, channel):
        try:
            # Initialize GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.CONTROL_PIN_A, GPIO.OUT)
            GPIO.setup(self.CONTROL_PIN_B, GPIO.OUT)

            # Set the demux channel based on the input
            if channel == 0:
                GPIO.output(self.CONTROL_PIN_A, GPIO.LOW)
                GPIO.output(self.CONTROL_PIN_B, GPIO.LOW)
            elif channel == 1:
                GPIO.output(self.CONTROL_PIN_A, GPIO.HIGH)
                GPIO.output(self.CONTROL_PIN_B, GPIO.LOW)
            elif channel == 2:
                GPIO.output(self.CONTROL_PIN_A, GPIO.LOW)
                GPIO.output(self.CONTROL_PIN_B, GPIO.HIGH)
            elif channel == 3:
                GPIO.output(self.CONTROL_PIN_A, GPIO.HIGH)
                GPIO.output(self.CONTROL_PIN_B, GPIO.HIGH)
            else:
                print("Invalid channel. Channel should be in the range 0-3.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def setSpeed(self, motor, speed):
        if motor == 0:
            # Set the channel for motor 0 (forward or backward)
            if speed >= 0:
                self.set_channel(0)  # Channel 00 for forward
            else:
                self.set_channel(1)  # Channel 01 for backward             
        elif motor == 1:
            # Set the channel for motor 1 (forward or backward)
            if speed >= 0:
                self.set_channel(2)  # Channel 10 for forward
            else:
                self.set_channel(3)  # Channel 11 for backward
        else:
            print("Invalid motor number. Use 0 for motor 0 or 1 for motor 1.")

        # Set the PWM
        self.set_pwm(abs(speed))
    
    def cleanup(self):
        try:
            # Stop the PWM and clean up the GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pwmPin, GPIO.OUT)
            pwm = GPIO.PWM(self.pwmPin, 1000)  # 1 kHz frequency
            pwm.stop()
            GPIO.cleanup()

            # Clean up control pins A and B
            GPIO.setup(self.CONTROL_PIN_A, GPIO.OUT)
            GPIO.setup(self.CONTROL_PIN_B, GPIO.OUT)
            GPIO.cleanup()
        except Exception as e:
            print(f"An error occurred during cleanup: {str(e)}")

