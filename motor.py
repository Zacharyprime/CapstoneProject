import RPi.GPIO as GPIO
import time

def motor_speed(speed, motorPins):

    pwmPin = motorPins[0]
    in1Pin = motorPins[1]
    in2Pin = motorPins[2]

    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwmPin, GPIO.OUT)
    GPIO.setup(in1Pin, GPIO.OUT)
    GPIO.setup(in2Pin, GPIO.OUT)

    # Set up PWM for speed control
    pwm = GPIO.PWM(pwmPin, 1000)  # 1000 Hz frequency
    pwm.start(0)

    # Set the motor direction based on speed
    if speed == 0:
        GPIO.output(in1Pin, 0)
        GPIO.output(in2Pin, 0)
        pwm.ChangeDutyCycle(0)
    elif speed > 0:
        GPIO.output(in1Pin, 0)
        GPIO.output(in2Pin, 1)
        pwm.ChangeDutyCycle(speed)
    else:
        GPIO.output(in1Pin, 1)
        GPIO.output(in2Pin, 0)
        pwm.ChangeDutyCycle(-speed)

    # Delay for a while (you can remove this if not needed)
    time.sleep(5)

    # Clean up and stop the motor
    pwm.stop()
    GPIO.cleanup()

def resetMotor(direction,speed,stopFlag,pwmPin,IN1,IN2):
    while(~stopFlag):
        motor_speed(speed*direction,pwmPin,IN1,IN2)

