import ethernet
import motorFunctions
import threading

if __name__ == "__main__":
    aeroflex = Aeroflex("Aeroflex_IP_Address")

    encoder_thread = threading.Thread(target=encoder_thread)
    encoder_thread.daemon = True  # Set as daemon to exit when the main program exits
    encoder_thread.start()

    #Define Pins
    pwmPin = 17 #The pin for the PWM output (that goes to the demux input)
    channelSelect = {17,18} #Select what channel to use for the demux
    motor1Encoder = {17,18} #Data pins for motor1 encoder
    motor2Encoder = {17,18} #Data pins for motor2 encoder

    # Disable RF output
    aeroflex.disable_rf_output()
    print("RF output disabled")

    # Grab the frequency
    current_frequency = aeroflex.retrieve_frequency()
    print(f"Current frequency: {current_frequency} MHz")

    # Enable RF output
    aeroflex.enable_rf_output()
    print("RF output enabled")

    #Turn all the way CW to the hard stop
    resetPosition()

    #Do the rough tuning (turning a prescribed number of turns)
    #Note both tuning functions must apply to both motors since refineTune can't work until both are complete.
    roughTune(current_frequency)

    #Precision Tuning
    refineTune()

    GPIO.cleanup()  # Cleanup GPIO on program exit