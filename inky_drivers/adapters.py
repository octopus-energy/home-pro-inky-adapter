import octave_tools.Octave_GPIO as GPIO
import time
import warnings
from datetime import timedelta


def adapter_busy_pin(
    timeout=40.0,
    busy_pin=17,
    start_time=None,
    last_change_time=None,
):
    """
    Rising edge detection on busy pin.
    Wait for the busy pin to go high (ACTIVE), with a timeout.
    If the pin is high initially, wait for the timeout period.
    Otherwise, poll the pin for a rising edge (low to high transition).
    """
    poll_interval_ms = timedelta(milliseconds=5)
    debounce_time_ms = timedelta(milliseconds=10)
    last_state = GPIO.OctaveGPIO.input(busy_pin)
    stable_state = last_state

    # If the busy pin is high initially, wait for the timeout period
    if last_state == 1:  # Assuming 1 is ACTIVE (HIGH)
        warnings.warn(
            f"Busy Wait: Held high. Waiting for {timeout:0.2f}s", stacklevel=1
        )
        time.sleep(timedelta(seconds=timeout))
        return

    # Polling loop to detect the rising edge or timeout
    while timedelta(seconds=time.time() - start_time) < timedelta(seconds=timeout):
        current_state = GPIO.OctaveGPIO.input(busy_pin)
        current_time = time.time() * 1000  # Current time in milliseconds

        # Debouncing logic: check if state remains stable for debounce period
        if current_state != last_state:
            # State change detected, reset debounce timer
            last_change_time = current_time
            last_state = current_state
        else:
            # If state has been stable long enough, register the change
            if current_time - last_change_time >= debounce_time_ms:
                if stable_state != current_state:
                    stable_state = current_state

                    # Check for a rising edge (low to high transition)
                    if stable_state == 1:  # Assuming 1 means rising edge
                        print("Rising edge detected!")
                        return

        # Sleep for the polling interval before checking again
        time.sleep(poll_interval_ms / 1000.0)

    # If we reach here, the timeout was reached without a rising edge
    warnings.warn(f"Busy Wait: Timed out after {timeout:0.2f}s", stacklevel=1)

    return


def set_pins(cs_pin=8, dc_pin=22, reset_pin=27, busy_pin=17):
    """
    Set up the GPIO pins for the Inky display.
    Accesses the GPIO pis via the octave GPIO api.
    """

    GPIO.OctaveGPIO.setup(cs_pin, GPIO.OUT)
    GPIO.OctaveGPIO.setup(dc_pin, GPIO.OUT)
    GPIO.OctaveGPIO.setup(reset_pin, GPIO.OUT)
    GPIO.OctaveGPIO.setup(busy_pin, GPIO.IN)

    GPIO.OctaveGPIO.output(cs_pin, GPIO.HIGH)
    GPIO.OctaveGPIO.output(dc_pin, GPIO.LOW)
    GPIO.OctaveGPIO.output(reset_pin, GPIO.HIGH)
