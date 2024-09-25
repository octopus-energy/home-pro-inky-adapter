import os
import requests

# Configurable API endpoint
host = os.getenv("IO_API_HOST")

# GPIO modes
GPIO = "GPIO"
BCM = "bcm"

# GPIO directions
IN = "in"
OUT = "out"

# Values
HIGH = 1
LOW = 0

# Mapping from Raspberry Pi GPIO numbers to Octave Expansion GPIO numbers
# Bank	IO	RP4	pin	port
# 2	    7	  22	15	39
# 2	    8	  19	35	40
# 2	    9	  6	  31	41
# 2	    10	17	11	42
# 2	    11	27	13	43
# 2	    12	16	36	44
# 2	    14	5	  29	46
# 2	    15	26	37	47
# 2	    16	20	38	48
# 2	    17	25	22	49
# 2	    18	24	18	50
# 2	    19	21	40	51

GPIO_CONVERSION = {
    22: 39,
    19: 40,
    6: 41,
    17: 42,
    27: 43,
    16: 44,
    5: 46,
    26: 47,
    20: 48,
    25: 49,
    24: 50,
    21: 51,
}


# Helper method to call API
def api_call(method, path, **kwargs):
    url = f"{host}/{path}"
    return requests.request(method, url, **kwargs)


class OctaveGPIO:  # Changed class name to avoid conflict

    # Convert Raspberry Pi GPIO to Octave Expansion GPIO
    @staticmethod
    def convert_gpio(channel):
        return GPIO_CONVERSION.get(channel, channel)

    # Set GPIO mode
    @staticmethod
    def setmode(mode):
        if mode == BCM:
            pass  # BCM mode
        else:
            raise ValueError("Invalid mode")

    # Set up individual GPIO channel
    @staticmethod
    def setup(channel, direction, initial=LOW):
        channel = OctaveGPIO.convert_gpio(channel)
        if direction == IN:
            api_call("POST", "gpio/direction", json={"gpio": channel, "dir": IN})
        elif direction == OUT:
            api_call("POST", "gpio/direction", json={"gpio": channel, "dir": OUT})
            api_call("POST", f"gpio/{channel}/value", json={"value": initial})
        else:
            raise ValueError("Invalid direction")

    # Input
    @staticmethod
    def input(channel):
        channel = OctaveGPIO.convert_gpio(channel)
        response = api_call("GET", f"gpio/{channel}/value")
        value = response.json().get("value", "0\n").strip()
        return int(value)

    # Output
    @staticmethod
    def output(channel, value):
        channel = OctaveGPIO.convert_gpio(channel)
        api_call("POST", f"gpio/{channel}/value", json={"value": value})

    # Additional methods like PWM, events, etc
    # ...
