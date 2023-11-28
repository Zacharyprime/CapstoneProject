import motor
import encoder

#Define Pins
motor1Pins = [17,18,19] # PWM | IN1 | IN2
motor2Pins = [20,21,22] # PWM | IN1 | IN2
motor1Encoder = {17,18} #Data pins for motor1 encoder
motor2Encoder = {17,18} #Data pins for motor2 encoder

buttonPin = 10 #button for input for doing ticks/turn

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Motor 1 Pins setup
for pin in motor1Pins:
    GPIO.setup(pin, GPIO.OUT)

# Motor 2 Pins setup
for pin in motor2Pins:
    GPIO.setup(pin, GPIO.OUT)

# Encoder pins setup
for pin in motor1Encoder.union(motor2Encoder):
    GPIO.setup(pin, GPIO.IN)

GPIO.setup(buttonPin,GPIO.IN)

#Setup Encoders
motor1Encoder = Encoder(motor1EncoderPins[0], motor1EncoderPins[1])
motor2Encoder = Encoder(motor2EncoderPins[0], motor2EncoderPins[1])


##MOTOR 1
printf("Press the button when the motor 1 has turned 10 times")

motor1Encoder.reset_encoder()
motor_speed(20,motor1Pins)

#Wait for the button to be pressed
while(~GPIO.input(buttonPin))

motor_speed(0,motor1Pins)
ticksPerTurn = motor1Encoder.get_position()/10

printf("Ticks per turn (M1):" + str(ticksPerTurn))


##MOTOR 2
printf("Press the button when the motor 2 has turned 10 times")

motor2Encoder.reset_encoder()
motor_speed(20,motor2Pins)

#Wait for the button to be pressed
while(~GPIO.input(buttonPin))

motor_speed(0,motor2Pins)
ticksPerTurn = motor2Encoder.get_position()/10

printf("Ticks per turn (M2):" + str(ticksPerTurn))

