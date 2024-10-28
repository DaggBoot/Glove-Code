# Importing modules
import serial
import pyautogui 
import time

# Initialising the serial comms
ser = serial.Serial('/dev/tty.usbmodem11401', 115200)

# Variable set up
crctr = 0
dataArr = [0,0,0,0] # pitch, roll, flex 1, flex 2
diff = [0,0,0,0] # pitch, roll, flex 1, flex 2
check_flag = False
dy = 0 
dx = 0 
rClick = False
lClick = False
l_count = 2
r_count = 2
drag = False
r_timer = 4
l_timer = 4

# Serial reading function
def read_sensor_data():
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        return data.split()
    else:
        return "error"

# Main function
if __name__ == "__main__":
    ser.write("y".encode()) # Code that sends request to start the PICO

    while True:
        try:
            ser.write("o".encode()) # Code that sends data requests
            data = read_sensor_data() # Reads data

            # Value offeset handler
            if check_flag == False and data != "error":
                if data[0] != 0:
                    diff[0] = float(data[0])
                if data[1] != 0:
                    diff[1] = float(data[0])
                check_flag = True

            if data != "error":
                # Assigns data to variables
                for i in range(0,4):
                    dataArr[i] = float(data[i]) - diff[i]

               
                # Translation Program
                if dataArr[0] >= -10 and dataArr[0] <= 10:
                    dy = 0
                elif (abs(dataArr[0]) > 5 and abs(dataArr[0]) <= 15):
                    if dataArr[0] < 0:
                        dy = 5
                    else:
                        dy = -5
                elif (abs(dataArr[0]) > 15 and abs(dataArr[0]) <= 30):
                    if dataArr[0] < 0:
                        dy = 25
                    else:
                        dy = -25
                elif (abs(dataArr[0]) > 30 and abs(dataArr[0]) <= 90):
                    if dataArr[0] < 0:
                        dy = 55
                    else:
                        dy = -55
                
                if dataArr[1] >= -5 and dataArr[1] <= 5:
                    dx = 0
                elif (abs(dataArr[1]) > 5 and abs(dataArr[1]) <= 15):
                    if dataArr[1] < 0:
                        dx = 5
                    else:
                        dx = -5
                elif (abs(dataArr[1]) > 15 and abs(dataArr[1]) <= 30):
                    if dataArr[1] < 0:
                        dx = 25
                    else:
                        dx = -25
                elif (abs(dataArr[1]) > 30 and abs(dataArr[1]) <= 90):
                    if dataArr[1] < 0:
                        dx = 55
                    else:
                        dx = -55
                
                # Click transaltion portion
                if dataArr[3] < 900 or dataArr[3] >= 1250:
                    l_count +=1
                    if l_count >= 7:
                        drag = True
                    elif l_count >= 5:
                        lClick = True
                        drag = False
                        l_count = 1
                else:
                    lClick = False
                    drag = False
                if dataArr[2] < 900 or dataArr[2] >= 1300:
                    r_count += 1
                    if r_count >= 5:
                        rClick = True
                        r_count = 1
                else:
                    rClick = False
                print(dataArr[2],dataArr[3],dy,dx,lClick,rClick)
            
            
            
            # Finally turning motion into action
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
