# Aeroflex Version 2

#imports
import time
import telnetlib

class V2Receiver:
    """A class to interface with a V2 Receiver."""
    def __init__(self, IP):
        self.IP = IP
        self.tn = telnetlib.Telnet(IP,8081,5)

    def close_telnet(self):
        """Close a Telnet session with the Receiver."""
        self.tn.close()

    def write_command(self, command):
        """Writes a command to the Receiver."""
        self.tn.write((command + "\n").encode())
        time.sleep(.25)

    def read_command(self):
        """Reads from the receiver until the end of the line."""
        response = list(self.tn.read_until(("\n").encode(), 2))
        response = ''.join(chr(v) for v in response)
        return response
    
    def special_read_until(self, desired):
        """Reads from the receiver until the desired character is found."""
        response = list(self.tn.read_until((desired).encode(), 2))
        response = ''.join(chr(v) for v in response)
        return response

    def clear(self):
        """Reads from the receiver until there is nothing left to be read."""
        tempread = self.read_command()
        while (tempread != ""):
            tempread = self.read_command()


class Aeroflex:
    """A class mirroring the functionality of an Aeroflex."""
    def __init__(self, IP):
        self.IP = IP
        self.tn = telnetlib.Telnet(IP,8081,5)

    def close_telnet(self):
        """Close a Telnet session with the Aeroflex."""
        self.write_command(":RF:GENerator:ENABle OFF")
        self.write_command(":MOD:GENerator:SOURce1:ENABle OFF")
        self.tn.close()

    def write_command(self, command):
        """Writes a command to the Aeroflex."""
        self.tn.write((command + "\n").encode())
        time.sleep(.25)

    def read_command(self, command):
        """Writes a command to the Aeroflex and reads the result."""
        self.tn.write((command + "\n").encode())
        time.sleep(.25)
        response = list(self.tn.read_until(("\n").encode(), 2))
        response = ''.join(chr(v) for v in response)
        return response

    def clear(self):
        tempread = self.read_command("")
        while (tempread != ""):
            tempread = self.read_command("")

    def RX_check_sensitivity(self, freq, first):
        """Check the receiver sensitivity."""
        if(first):
            # Assign a volume of 0
            self.write_command(":ASSign:VOLume 0")

            # Turn off RF generator
            self.write_command(":RF:GENerator:ENABle OFF")

            # Turn off Mod 1 generator
            self.write_command(":MOD:GENerator:SOURce1:ENABle OFF")

            # Turn off Mod 2 generator
            self.write_command(":MOD:GENerator:SOURce2:ENABle OFF")

            # Turn off Mod 3 generator
            self.write_command(":MOD:GENerator:SOURce3:ENABle OFF")

            # Display the "Generators" tile
            self.write_command(":DISPlay:TILE1:NAME \"Generators\"")

            # Display the "Channel Analyzer" tile
            self.write_command(":DISPlay:TILE4:NAME \"Channel Analyzer\"")

            # Display the "Meters" tile
            self.write_command(":DISPlay:TILE3:NAME \"Meters\"")

            # Display the "Analyzers" tile
            self.write_command(":DISPlay:TILE2:NAME \"Analyzers\"")

            # Set the duplex offset value to 0 Hz
            self.write_command(":CONFigure:OFFSet:DUPLex:VALue 0.0 MHz")

            # Set the RF generator to modulate AM
            self.write_command(":RF:GENerator:MOD AM")

            # Unlock the duplex offset
            self.write_command(":CONFigure:OFFSet:DUPLex:LOCK 0")

            # Enable the Mod 1 generator
            self.write_command(":MOD:GENerator:SOURce1:ENABle ON")

            # Mod generator at 1.004 KHz
            self.write_command(":MOD:GENerator:SOURce1:FREQuency 1004Hz")

            # 30% modulation
            self.write_command(":MOD:GENerator:SOURce1:AM 30%")

            # Sine wave shape
            self.write_command(":MOD:GENerator:SOURce1:SHAPe SINE")

            # 15KHz filter
            self.write_command(":AF:ANALyzer:MFILter LP4")

            # Audio units in dBm
            self.write_command(":CONFigure:AF:ANALyzer:LEVel:AUDio:UNIts dBm")

            # CMESS Filter
            self.write_command(":CONFigure:AF:MFILter CMESs")

            # Required for correct operation
            self.write_command(":CONFigure:AF:ANALyzer:SOURce:VARiable:LOAD:ENABle 0")

            # Use Audio source 1
            self.write_command(":CONFigure:AF:ANALyzer:SOURce AUD1")

            # Required for correct operation
            self.write_command(":AF:ANALyzer:LEVel:HOLD:ENABle 0")

            # Do the measurment type to S/N
            self.write_command(":AF:ANALyzer:NTYPe SN")

            # Required for correct operation
            self.write_command(":CONFigure:AF:ANALyzer:SNR:MODE 1")

            # Required for correct operation
            self.write_command(":AF:ANALyzer:SNR:HOLD:ENABle 0")

            # Take five samples
            self.write_command(":CONFigure:AF:ANALyzer:SNR:AVERage 3")

            # Turn on RF generator
            self.write_command(":RF:GENerator:ENABle ON")

            # RCI meter mode to fast
            self.write_command(":SYSTem:RCI:METER:MODE FAST")

        # Set frequency to operating frequency
        self.write_command(":RF:GENerator:FREQuency " + str(freq) + "MHz")

        # Set RF Analyzer frequency to operating frequency
        self.write_command(":RF:ANALyzer:FREQuency " + str(freq) + "MHz")
        
        # Set RF level to -108dBm
        self.write_command(":RF:GENerator:LEVel -108dBm")

        ################ Begin searching for the sensitivity ################
        time.sleep(5)
        level = -108.0
        increments = [0.5, 0.1]
        S_N_string = self.read_command(":FETCh:AF:ANALyzer:SNR?") #Measure the signal to noise ratio in dBm
        S_N_string_list = S_N_string.split(',') #We get back some data separated by commas, so separate them
        S_N = S_N_string_list[3] #Grab and store the SNR
        S_N = S_N[0:-1] #Get rid of the endline character
        for increment in increments:
            while (float(S_N) <= 10.0): #If S/N is less than 10.0, then increase the RF level and read again
                level += increment
                if level > -80: #If the sensitivity is too high, don't continue and close the program
                    self.close_telnet()
                    exit(1)
                self.write_command(":RF:GENerator:LEVel " + str(level) + "dBm")
                time.sleep(5) #Wait 5 seconds for the measurment to stabilize
                S_N_string = self.read_command(":FETCh:AF:ANALyzer:SNR?") #Measure the signal to noise ratio in dBm
                S_N_string_list = S_N_string.split(',') #We get back some data separated by commas, so separte them
                while(len(S_N_string) < 4):
                    S_N_string = self.read_command(":FETCh:AF:ANALyzer:SNR?") #Measure the signal to noise ratio in dBm
                    S_N_string_list = S_N_string.split(',') #We get back some data separated by commas, so separte them
                S_N = S_N_string_list[3] #Grab and store the SNR
                S_N = S_N[0:-1] #Get rid of the endline character
            if increment != 0.1: #If we went too far, back up then start again at a smaller increment
                level -= increment
                S_N = 0
        ################ End searching for the sensitivity ################

        output = "Measured sensitivy is:    " + str(level) + "dBm"
        print(output)
        return str(round(level,4))

    def RX_check_squelch(self, freq):
        """Check the receiver squelch threshold."""

        # Turn on RF generator
        self.write_command(":RF:GENerator:ENABle ON")
        
        # RF out on GEN
        self.write_command(":RF:GENerator:PORT GEN")

        # Turn off Gen Offset
        self.write_command(":CONFigure:OFFSet:GENerator:ENABle OFF")

        # Set frequency to operating frequency
        self.write_command(":RF:GENerator:FREQuency " + str(freq) + "MHz")

        # Set RF level to -115dBm
        self.write_command(":RF:GENerator:LEVel -115dBm")

        # Duplex offset value to 0
        self.write_command(":CONFigure:OFFSet:DUPLex:VALue 0MHz")

        # Set RF mod type to AM
        self.write_command(":RF:GENerator:MOD AM")

        # Unlock Dx offset
        self.write_command(":CONFigure:OFFSet:DUPLex:LOCK OFF")

        # Turn on Mod 1
        self.write_command(":MOD:GENerator:SOURce1:ENABle ON")

        # Set Mod 1 frequency to 1004Hz
        self.write_command(":MOD:GENerator:SOURce1:FREQuency 1004Hz")

        # Set Mod 1 depth to 30%
        self.write_command(":MOD:GENerator:SOURce1:AM 30%")

        # Set Mod 1 waveform shape to SINE
        self.write_command(":MOD:GENerator:SOURce1:SHAPe SINE")

        # Turn off Mod 2
        self.write_command(":MOD:GENerator:SOURce2:ENABle OFF")

        # Turn off Mod 3
        self.write_command(":MOD:GENerator:SOURce3:ENABle OFF")

        # Set audio filter to LP 15kHz
        self.write_command(":AF:ANALyzer:MFILter LP4")

        # Set audio units to dBm
        self.write_command(":CONFigure:AF:ANALyzer:LEVel:AUDio:UNIts dBm")

        # Set Psoph Filter to CMESS
        self.write_command(":CONFigure:AF:MFILter CMESs")

        # Set internal load to 600Ohms
        self.write_command(":CONFigure:AF:ANALyzer:SOURce:LOAD UNB600")

        # Set audio source to 1
        self.write_command(":CONFigure:AF:ANALyzer:SOURce AUD1")

        # Disable external load
        self.write_command(":CONFigure:AF:ANALyzer:SOURce:VARiable:LOAD:ENABLe OFF")
        
        # Set AF measurement SINAD to 1
        self.write_command(":CONFigure:AF:ANALyzer:SINad:AVERage 1")

        # Ask user to turn on squelch
        input("Please verify that squelch is on, then press ENTER:")

        ################ Begin searching for the squelch threshold ################
        time.sleep(2)
        level = -115.0
        increments = [2.0, 0.1]
        threshold_string = self.read_command(":FETCh:AF:ANALyzer:LEVel?") #Measure the signal to noise ratio in dBm
        threshold_string_list = threshold_string.split(',')
        threshold = threshold_string_list[3]
        for increment in increments:
            while (level <= 50.0): #If AF level is less than 50.0, then increase the RF level and read again
                level += increment
                self.write_command(":RF:GENerator:LEVel " + str(level) + "dBm")
                time.sleep(2)
                threshold_string = self.read_command(":FETCh:AF:ANALyzer:LEVel?") #Measure the signal to noise ratio in dBm
                threshold_string_list = threshold_string.split(',')
                threshold = threshold_string_list[3]
            if increment > 0.1: #If we went too far, back up then start again at a smaller increment
                level -= increment
        ################ End searching for the squelch threshold ################

        ################ Begin searching for the squelch close ################
        time.sleep(2)
        while (level >= 50.0): #If AF level is less than 50.0, then increase the RF level and read again
            level -= 0.1
            self.write_command(":RF:GENerator:LEVel " + str(level) + "dBm")
            time.sleep(2)
            close_string = self.read_command(":FETCh:AF:ANALyzer:LEVel?")
            close_string_list = close_string.split(',')
            close = close_string_list[3]
        ################ End searching for the squelch threshold ################

        output1 = "Measured squelch threshold is:    " + str(threshold) + "dBm"
        output2 = "Measured squelch close is:    " + str(close) + "dBm"
        print(output1)
        print(output2)

    def RX_check_audio_output(self, freq):
        """Check the receiver audio output."""
        
        # Turn on RF generator
        self.write_command(":RF:GENerator:ENABle ON")
        
        # RF out on GEN
        self.write_command(":RF:GENerator:PORT GEN")

        # Turn off Gen Offset
        self.write_command(":CONFigure:OFFSet:GENerator:ENABle OFF")

        # Set frequency to operating frequency
        self.write_command(":RF:GENerator:FREQuency " + str(freq) + "MHz")

        # Set RF level to -73dBm
        self.write_command(":RF:GENerator:LEVel -73dBm")

        # Duplex offset value to 0
        self.write_command(":CONFigure:OFFSet:DUPLex:VALue 0MHz")

        # Set RF mod type to AM
        self.write_command(":RF:GENerator:MOD AM")

        # Unlock Dx offset
        self.write_command(":CONFigure:OFFSet:DUPLex:LOCK OFF")

        # Turn on Mod 1
        self.write_command(":MOD:GENerator:SOURce1:ENABle ON")

        # Set Mod 1 frequency to 1004Hz
        self.write_command(":MOD:GENerator:SOURce1:FREQuency 1004Hz")

        # Set Mod 1 depth to 30%
        self.write_command(":MOD:GENerator:SOURce1:AM 30%")

        # Set Mod 1 waveform shape to SINE
        self.write_command(":MOD:GENerator:SOURce1:SHAPe SINE")

        # Turn off Mod 2
        self.write_command(":MOD:GENerator:SOURce2:ENABle OFF")

        # Turn off Mod 3
        self.write_command(":MOD:GENerator:SOURce3:ENABle OFF")

        # Set audio filter to LP 15kHz
        self.write_command(":AF:ANALyzer:MFILter LP4")

        # Set audio units to dBm
        self.write_command(":CONFigure:AF:ANALyzer:LEVel:AUDio:UNIts dBm")

        # Set Psoph Filter to CMESS
        self.write_command(":CONFigure:AF:MFILter CMESs")

        # Set internal load to 600Ohms
        self.write_command(":CONFigure:AF:ANALyzer:SOURce:LOAD UNB600")

        # Set audio source to 1
        self.write_command(":CONFigure:AF:ANALyzer:SOURce AUD1")

        # Disable external load
        self.write_command(":CONFigure:AF:ANALyzer:SOURce:VARiable:LOAD:ENABLe OFF")
        
        # Set AF measurement SNR to 5
        self.write_command(":CONFigure:AF:ANALyzer:SNR:AVERage 5")

        # Measure the audio output level
        level_string = self.read_command(":FETCh:AF:ANALyzer:LEVel?")
        level_string_list = level_string.split(',')
        level = level_string_list[3]

        output = "Measured audio level is:    " + level + "dBm"
        print(output)

    def RX_check_all(self, freq, measure_osc_freq):
        """Perform all receiver checks (or skip oscillator frequency if desired)."""
        if (measure_osc_freq):
            self.RX_check_osc_frequency()
        self.RX_check_sensitivity(freq)
        self.RX_check_squelch(freq)
        self.RX_check_audio_output(freq)

    def TX_check_frequency(self, freq, first=False):
        """Check the transmitter operating frequency."""
        
        if first:
            # Turn off Autotune
            self.write_command(":RF:ANALyzer:FMODe MANual")

            # Set RF in to T/R
            self.write_command(":RF:ANAL:PORT TR")

            # Analyzer offset to off
            self.write_command(":CONFigure:OFFSet:ANALyzer:ENABle OFF")

        #Set the frequency manually
        self.write_command(":RF:ANALyzer:FREQuency " + str(freq) + "MHz")

        print("Measuring...")

        # Measure frequency
        time.sleep(4)
        freq_string = self.read_command(":FETCh:RF:ANALyzer:FREQuency?")
        freq_string_list = freq_string.split(',')
        freq = freq_string_list[1]
        freq = freq[0:3] + '.' + freq[3:9] #Split the freq string into MHz

        output = "Measured frequency is:    " + freq + "MHz\n"
        print(output)
        return freq

    def TX_check_power_output(self, freq, first=False):
        """Check the trasnmitter output power."""
        
        #If only checking power once and not in a loop, do these
        if (first):
            # Turn off Autotune
            self.write_command(":RF:ANALyzer:FMODe MANual")

            # Set RF in to T/R
            self.write_command(":RF:ANAL:PORT TR")

            # Analyzer offset to off
            self.write_command(":CONFigure:OFFSet:ANALyzer:ENABle OFF")

            # Power measurement type to broadband
            self.write_command(":RF:ANALyzer:PMType BB")

        #Set the frequency manually
        self.write_command(":RF:ANALyzer:FREQuency " + str(freq) + "MHz")

        print("Measuring...")

        # Measure power
        time.sleep(2)
        power_string = self.read_command(":FETCh:RF:ANALyzer:TRBPower? W")
        power_string_list = power_string.split(',')
        if len(power_string_list) < 4:
            power_string = self.read_command(":FETCh:RF:ANALyzer:TRBPower? W")
            power_string_list = power_string.split(',')
        power = str(power_string_list[3])
        power = power[0:-1]

        output = "Measured power is:    " + power + "W"
        print(output)
        return power

    def TX_check_tone_modulation(self, freq, first=False):
        """Check the transmitter modulation on tone."""
        
        if (first):
            # Turn off RF generator
            self.write_command(":RF:GENerator:ENABle OFF")

            # Turn off Mod 1
            self.write_command(":MOD:GENerator:SOURce1:ENABle OFF")

            # Turn off Mod 2
            self.write_command(":MOD:GENerator:SOURce2:ENABle OFF")

            # Turn off Mod 3
            self.write_command(":MOD:GENerator:SOURce3:ENABle OFF")

            # Turn on AF1 generator
            self.write_command(":AF:GENerator:SOURce1:ENABle ON")

            # AF1 frequency to 1004Hz
            self.write_command(":AF:GENerator:SOURce1:FREQuency 1004Hz")

            # AF1 level to -8.0dBm
            self.write_command(":AF:GENerator:SOURce1:LEVel -8dBm")

            # AF1 waveform shape to sine
            self.write_command(":AF:GENerator:SOURce2:SHAPe SINE")

            # Turn off AF2
            self.write_command(":AF:GENerator:SOURce2:ENABle OFF")

            # Turn off AF3
            self.write_command(":AF:GENerator:SOURce3:ENABle OFF")

            # Output on function generator
            self.write_command(":CONFigure:PORT:FGEN FGEN")

            # Output impedance to 600Ohms
            self.write_command(":CONFigure:IMPedance:AF:GENerator 600OHMS")

            # Turn off Autotune
            self.write_command(":RF:ANALyzer:FMODe MANual")

            # Set RF in to T/R
            self.write_command(":RF:ANAL:PORT TR")

            # Analyzer offset to off
            self.write_command(":CONFigure:OFFSet:ANALyzer:ENABle OFF")

        #Set the frequency manually
        self.write_command(":RF:ANALyzer:FREQuency " + str(freq) + "MHz")

        print("Measuring...")

        # Measure modulation
        time.sleep(2)
        modulation_string = self.read_command(":FETCh:MOD:ANALyzer:AM?")
        modulation_string_list = modulation_string.split(',')
        modulation = modulation_string_list[3]

        output = "Measured modulation is:    " + modulation + "%"
        print(output)
        return modulation

    def TX_check_all(self):
        """Perform all transmitter checks."""
        self.TX_check_frequency(True)
        self.TX_check_power_output(True)
        self.TX_check_tone_modulation(True)