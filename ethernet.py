#imports
import time
import telnetlib

class Aeroflex:
    """A class mirroring the functionality of an Aeroflex."""
    def __init__(self, IP):
        self.IP = IP
        self.tn = telnetlib.Telnet(IP, 8081, 5)

    def close_telnet(self):
        """Close a Telnet session with the Aeroflex."""
        self.write_command(":RF:GENerator:ENABle OFF")
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

    def disable_rf_output(self):
        """Disable RF output on the Aeroflex."""
        self.write_command(":RF:GENerator:ENABle OFF")

    def enable_rf_output(self):
        """Enable RF output on the Aeroflex."""
        self.write_command(":RF:GENerator:ENABle ON")

    def get_initial_frequency(self, desired_freq):
        """Retrieve the initial frequency from the Aeroflex and verify RF output is disabled."""
        self.disable_rf_output()  # Ensure RF output is disabled
        current_freq = self.retrieve_frequency()  # Get the current frequency
        if current_freq == desired_freq:
            return current_freq
        else:
            print("Error: Initial frequency does not match the desired frequency.")
            return None

    def retrieve_frequency(self):
        """Retrieve the frequency from the Aeroflex."""
        response = self.read_command(":RF:GENerator:FREQuency?")
        return int(response)
    
    def retrieve_frequency(self):
        """Retrieve the frequency from the Aeroflex."""
        response = self.read_command(":SA:MARKer:MKR1:LEVel?")
        return int(response)

    def getPWR(self):
        """Retrieve the frequency from the Aeroflex."""
        response = self.read_command(":SA:MARKer:MKR1:LEVel?")
        return response

