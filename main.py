import ethernet
import encoder
import motor
import threading
import motor
import RPi.GPIO as GPIO
import time

## Testing needed
# + Check of motor directions are all good, negative was assumed to be towards the hard stop
# + The value of ticksPerTurn in roughTune (see encoderTest.py)
# + The value of delta in fineTune (trial and error)
# + The speed of the motor for each stage (arbitrary values picked initially)
# + Convergence threshold for fineTune

#-----SET THE PINS AND IP ADDRESS CORRECTLY------

def resetPosition(currentSensor,motorPins,speed=10):
    while(GPIO.input(currentSensor)):
        motor_speed(-1*speed,motorPins)

#Turns the motors a prescribed amount based on frequency
#Note: Uses a curve fit of the prescribed data given in the manual
def roughTune(frequency,motorPins,encoder):
    #Ticks of the encoder in a single turn (experimental value)
    ticksPerTurn = 298 

    #Applies a curve fit to the data given in the manual
    #The data is seperated by VHF and UHF, so a seperate curve fit is used for both
    if(frequency>=110 and frequency<=170):
        printf("VHF detected, applying rough tune")
        #Curve fit (2nd order polynomial) for VHF data
        turnsTarget = (-29.6)+(0.449)*frequency-(1.28*10^-3)*frequency^2 

    elif(frequency>210 and frequency<=400):
        printf("UHF detected, applying rough tune")
        #Curve fit (3rd order polynomial) for UHF data
        turnsTarget = (-64)+(0.543)*frequency-(1.4*10^-3)*frequency^2 + (1.29*10^-6)*frequency^3 
    
    #Error conditions
    elif(frequency<110):
        printf("Frequency too low, outside of VHF band")
    elif(frequency>400):
        printf("Frequency too high, outside of UHF band")
    else
        printf("Frequency invalid, range (150,225) is not defined by manual")

    #Set the encoder to zero so we are tracking from start
    encoder.reset_encoder()

    #Turn until we reached the spot
    while(abs(encoder.get_position())/ticksPerTurn < turnsTarget):
        motor_speed(20,motorPins)
    
    motor_speed(0,motorPins)

def moveMotor(ticks,speed,motorPins,encoder):
    #Set the encoder to zero so we are tracking from start
    encoder.reset_encoder()

    #Turn until we reached the spot
    while(abs(encoder.get_position()) < ticks):
        motor_speed(speed,motorPins)
    motor_speed(0,motorPins)

#Returns an averaged power
def avgPower(aeroflex, samples=10, spacing=1):
    sum = 0
    while(nn<samples):
        sum += aeroflex.getPWR()
        time.sleep(spacing)
    return sum/samples

def optimizeMotor(aeroflex,motorPins,encoder,moveSpeed=20,delta=20):
    #Make sure the motor is stopped
    motor_speed(0,motorPins)

    #Take a power measurement at the center (for reference)
    centerPower = avgPower(aeroflex)

    #Move motor 1 in one direction, take a measurement
    moveMotor(delta,moveSpeed,motorPins,encoder)
    meas1 = avgPower(aeroflex)-centerPower

    #Move motor 1 in the other direction, take another measurment
    #This is done in one sweep instead of centering to avoid errors (small steps are prob less accurate)
    moveMotor(2*delta,-1*moveSpeed,motorPins,encoder) #2 * deltaTick so that it goes to the other side of the center.
    meas2 = avgPower(aeroflex)-centerPower

    #Return the motor to center
    moveMotor(delta,moveSpeed,motorPins,encoder)

    #Decide which direction we need to go to increase the power (or if we should stay still)
    if(meas1 > 0 and meas2 > 0): #Both measurements make power go up
        if(meas1>=meas2): #Positive was better
            moveMotor(delta,moveSpeed,motorPins,encoder)
        else: #Negative was better
            moveMotor(delta,-1*moveSpeed,motorPins,encoder)

    elif(meas1 > 0): #Only the positive direction caused an increase
        moveMotor(delta,moveSpeed,motorPins,encoder)

    elif(meas2 > 0): #Only the negative direction caused an increase
        moveMotor(delta,-1*moveSpeed,motorPins,encoder)

    else: #Neither direction would benefit us
        motor_speed(0,motorPins)
        return 1
    
    #Make sure the motor is stopped after we finish
    motor_speed(0,motorPins)
    return 0

def fineTune(aeroflex,motor1Pins,motor2Pins,encoder1,encoder2,convergethreshold=5):
    #These will likely be dynamically adjusted in final implementation
    delta = 40 #How much should the motors move to sample (at first)
    convergeThreshold = 5 #Somewhat arbitrary, how small should deltaTick get before we call it good

    #This runs the optimize motor function for both directions
    #If that function ends up not needing to move the motors, it returns 1 instead of 0
    #If both functions returned a 1, we cannot improve our results by moving the motors <=> calibrated
    while(delta < convergeThreshold):
        if(optimizeMotor(aeroflex,motor1Pins,encoder1,moveSpeed,delta) and optimizeMotor(aeroflex,motor2Pins,encoder2,moveSpeed,delta)):
            delta = delta/2

if __name__ == "__main__":
    aeroflex = Aeroflex("169.254.125.1")

    #Define Pins
    motor1Pins = [17,18,19] # PWM | IN1 | IN2
    motor2Pins = [20,21,22] # PWM | IN1 | IN2
    motor1EncoderPins = {17,18} #Data pins for motor1 encoder
    motor2EncoderPins = {17,18} #Data pins for motor2 encoder
    currentSensor = 1 #Current detection pin

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

    # Current sensor pin setup
    GPIO.setup(currentSensor, GPIO.IN)

    #Initialize Encoders
    motor1Encoder = Encoder(motor1EncoderPins[0], motor1EncoderPins[1])
    motor2Encoder = Encoder(motor2EncoderPins[0], motor2EncoderPins[1])

    # Disable RF output
    aeroflex.disable_rf_output()
    print("RF output disabled")

    # Grab the frequency
    current_frequency = aeroflex.retrieve_frequency()
    print(f"Current frequency: {current_frequency} MHz")

    ##RESET POSITIONS##
    #Turn all the way CW to the hard stop
    resetPosition(currentSensor,motor1Pins) #Reset motor 1
    while(not GPIO.input(currentSensor)) #Wait for the current sensor to return
    resetPosition(currentSensor,motor2Pins) #Reset motor 2
    printf("Position Reset Complete.")

    ##ROUGH TUNE##
    #Do the rough tuning (turning a prescribed number of turns)
    roughTune(current_frequency,motor1Pins,motor1Encoder)
    roughTune(current_frequency,motor2Pins,motor2Encoder)
    printf("Rough Tune complete.")

    # Enable RF output
    aeroflex.enable_rf_output()
    print("RF output enabled")

    ##FINE TUNE##
    fineTune(aeroflex,motor1Pins,motor2Pins,motor1Encoder,motor2Encoder)
    printf("Fine Tune Complete.")

    GPIO.cleanup()  # Cleanup GPIO on program exit