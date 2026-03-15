"""
Glove Mouse Controller

This script reads sensor data from a microcontroller (e.g., Raspberry Pi Pico) via serial
and translates hand movements and finger flexes into mouse movements and clicks using PyAutoGUI.

Sensors:
- pitch (tilt forward/back)
- roll (tilt left/right)
- flex 1 (right click / drag)
- flex 2 (left click / drag)

Usage:
- Connect the microcontroller and update the serial port.
- Run the script: python glove_mouse.py
"""
# Importing modules
import serial
import pyautogui
import time

# Constants

SERIAL_PORT = '/dev/tty.usbmodem11401'
BAUD_RATE = 115200

L_FLEX_THRESHOLD = (900, 1250)
R_FLEX_THRESHOLD = (900, 1300)
CLICK_COUNT = 5
DRAG_COUNT = 7
TIMER_RESET = 4

DEBUG = True

# Variable set up
crctr = 0
dataArr = [0, 0, 0, 0]  # pitch, roll, flex 1, flex 2
diff = [0, 0, 0, 0]  # pitch, roll, flex 1, flex 2
check_flag = False
dy = 0
dx = 0
rClick = False
lClick = False
l_count = 2
r_count = 2
drag = False
r_timer = TIMER_RESET
l_timer = TIMER_RESET


# Initialising the serial comms
ser = serial.Serial('/dev/tty.usbmodem11401', 115200)

# Helper functions


def read_sensor_data() -> list[str] | str:
    """Reads a line of sensor data from the serial port.
    Returns split data from the microcontroller, or raises an error if no data is available.
    """
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        return data.split()
    else:
        raise "error"


def map_pitch_to_dy(pitch: float) -> int:
    """
    Converts a pitch value from the glove into a vertical mouse movement (dy).
    Returns the number of pixels to move vertically.

    Args:
        pitch (float): The pitch value from the glove.
    """
    if -10 <= pitch <= 10:
        return 0
    elif 5 < abs(pitch) <= 15:
        return 5 if pitch < 0 else -5
    elif 15 < abs(pitch) <= 30:
        return 25 if pitch < 0 else -25
    elif 30 < abs(pitch) <= 90:
        return 55 if pitch < 0 else -55
    return 0


def map_roll_to_dx(roll: float) -> int:
    """
    Converts a roll value from the glove into a horizontal mouse movement (dx).
    Returns the number of pixels to move horizontally.

    Args:
        roll (float): The roll value from the glove.
    """
    if -5 <= roll <= 5:
        return 0
    elif 5 < abs(roll) <= 15:
        return 5 if roll < 0 else -5
    elif 15 < abs(roll) <= 30:
        return 25 if roll < 0 else -25
    elif 30 < abs(roll) <= 90:
        return 55 if roll < 0 else -55
    return 0


if __name__ == "__main__":
    """
        Main loop for the glove mouse controller. Initializes the serial connection,
        reads sensor data continuously, maps pitch and roll to mouse movement,
        and handles clicks and drag actions based on finger flexes.
    """

    ser.write("y".encode())  # Code that sends request to start the PICO

    while True:
        try:
            ser.write("o".encode())  # Code that sends data requests
            data = read_sensor_data()  # Reads data

            # Ensure we have enough data
            if data == "error" or len(data) < 4:
                continue

            # Value offeset handler
            if not check_flag:
                if data[0] != 0:
                    diff[0] = float(data[0])
                if data[1] != 0:
                    diff[1] = float(data[0])
                check_flag = True

            # Assigns data to variables
            for i in range(0, 4):
                dataArr[i] = float(data[i]) - diff[i]

            #  Translation Program
            dy = map_pitch_to_dy(dataArr[0])
            dx = map_roll_to_dx(dataArr[1])

            # Click transaltion portion

            if dataArr[3] < L_FLEX_THRESHOLD[0] or dataArr[3] >= L_FLEX_THRESHOLD[1]:
                l_count += 1
                if l_count >= DRAG_COUNT:
                    drag = True
                elif l_count >= CLICK_COUNT:
                    lClick = True
                    drag = False
                    l_count = 1
            else:
                lClick = False
                drag = False

            if dataArr[2] < R_FLEX_THRESHOLD[0] or dataArr[2] >= R_FLEX_THRESHOLD[1]:
                r_count += 1
                if r_count >= CLICK_COUNT:
                    rClick = True
                    r_count = 1
            else:
                rClick = False

            if DEBUG:
                print(dataArr[2], dataArr[3], dy, dx, lClick, rClick)

            if lClick and rClick:
                if dy < -5:
                    pyautogui.scroll(10)
                elif dy > 5:
                    pyautogui.scroll(-10)
            elif rClick:
                r_timer -= 1
                if r_timer == 0:
                    r_timer = 4
                    pyautogui.click(button="right")
                    time.sleep(.2)
            if lClick:
                l_timer -= 1
                if l_timer == 0:
                    l_timer = 4
                    pyautogui.click()
                    time.sleep(.2)
            elif drag:
                pyautogui.dragRel(dx, dy, duration=0.005)
            else:
                pyautogui.moveRel(dx, dy)

        except KeyboardInterrupt:
            ser.close()
            print("Serial connection closed.")
        finally:
            ser.close()
            print("Serial connection closed.")
